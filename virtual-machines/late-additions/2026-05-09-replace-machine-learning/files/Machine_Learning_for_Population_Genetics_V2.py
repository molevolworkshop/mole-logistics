import argparse
import msprime # version 1.3.3
import matplotlib.pyplot as plt # version 3.9.2
import random
import numpy as np # version 2.0.2
from sklearn.model_selection import train_test_split # version 1.7.2
from sklearn.metrics import confusion_matrix, accuracy_score 
from keras.utils import to_categorical # version 3.6.0
from tensorflow.keras import layers, optimizers, models # version 2.18.0


def parse_args():
    parser = argparse.ArgumentParser(description="Simulate data, train & test a CNN.")
    
    parser.add_argument("--simulate", action="store_true",help="If set, simulate data.")
    parser.add_argument("--n_reps", type=int, default=100, help="Number of replicates (default: 100).")
    
    parser.add_argument("--train", action="store_true",help="If set, train model.")
    parser.add_argument('--epochs', type=int, default=10, help="Number of epochs to train CNN.")
    parser.add_argument('--batch_size', type=int, default=64, help="Batch size to use during training.")
    parser.add_argument('--layers', type=int, default=2, help="Number of fully connected layers to use (1-4).")
    parser.add_argument('--dropout', type=float, default=0.0, help="Dropout rate to use (0.0-1.0).")
    parser.add_argument('--learning_rate', type=float, default=0.00001, help="Learning rate for training.")

    parser.add_argument("--test", action="store_true",help="If set, test CNN.")
    
    return parser.parse_args()    

def divergence(tdiv, ne_anc, ne_1, ne_2):  
    """This function defines a divergence-only model. 
        It takes as input several parameters:
        tdiv (divergence time in generations)
        ne_anc (the effective population size of the ancestral population)
        ne_1 (the effective population size of population 1)
        ne_2 (the effective population size of population 2)"""

     # set up msprime model
    demography = msprime.Demography()
    demography.add_population(name="A", initial_size = ne_1) # population 1
    demography.add_population(name="B", initial_size = ne_2) # population 2
    demography.add_population(name="C", initial_size = ne_anc) # ancestral population
    demography.add_population_split(time=tdiv, derived=["A", "B"], ancestral="C") # divergence
    return(demography)

def geneflow(tdiv, migrate, ne_anc, ne_1, ne_2):
    """This function defines a secondary contact model. 
        It takes as input several parameters:
        tdiv (divergence time in generations)
        migrate (the rate of migration between populations)
        ne_anc (the effective population size of the ancestral population)
        ne_1 (the effective population size of population 1)
        ne_2 (the effective population size of population 2)"""

     # set up msprime model
    demography = msprime.Demography()
    demography.add_population(name="A", initial_size = ne_1) # population 1
    demography.add_population(name="B", initial_size = ne_2) # population 2
    demography.add_population(name="C", initial_size = ne_anc) # ancestral population
    demography.set_symmetric_migration_rate(populations=["A", "B"], rate=migrate) # start migration
    demography.add_symmetric_migration_rate_change(time=tdiv//2, populations=["A", "B"], rate=0) # set migration rate to zero
    demography.add_population_split(time=tdiv, derived=["A", "B"], ancestral="C") # divergence (migration stops)
    return(demography)

def simulate_data(tdiv_prior, ne_prior, migrate_prior, sample_size, seq_len, mu, rec_rate, replicates):

    print("=" * 80)
    print("Simulating data for training and testing")
    print(f"  models: divergence, geneflow")
    print(f"  replicates per model: {replicates}")
    print(f"  sequence length: {seq_len:,}")
    print("=" * 80)

    # lists for storing matrices, responses
    all_sfs = []
    all_responses = []

    
    for model in ['divergence', 'geneflow']:
        
        for i in range(replicates):

            # draw parameters from priors
            this_tdiv = random.randint(tdiv_prior[0], tdiv_prior[1])
            this_ne_anc = random.randint(ne_prior[0], ne_prior[1])
            this_ne_1 = random.randint(ne_prior[0], ne_prior[1])
            this_ne_2 = random.randint(ne_prior[0], ne_prior[1])
            if model == "geneflow":
                this_migrate = np.random.uniform(low=migrate_prior[0], high=migrate_prior[1])
               
            # get our demography (using the function defined above)  
            if model == "divergence":
                demography = divergence(tdiv=this_tdiv, ne_anc=this_ne_anc, ne_1=this_ne_1, ne_2=this_ne_2)
            elif model == "geneflow":
                demography = geneflow(tdiv=this_tdiv, migrate=this_migrate, ne_anc=this_ne_anc, 
                                    ne_1=this_ne_1, ne_2=this_ne_2)

            # simulate tree sequences
            ts = msprime.sim_ancestry(samples={"A": sample_size, "B": sample_size}, 
                            demography = demography, sequence_length=seq_len, recombination_rate = rec_rate)
    
            # simulate mutations
            mts = msprime.sim_mutations(ts, rate=mu)

            # SFS
            sfs = mts.allele_frequency_spectrum(sample_sets=[mts.samples(0), mts.samples(1)], span_normalise=False, polarised=True)
    
            # get responses
            if model == 'divergence':
                response = 0
            elif model == 'geneflow':
                response = 1
    
            # append to lists
            all_sfs.append(sfs)
            all_responses.append(response)
    
    # convert lists to numpy arrays
    all_sfs = np.stack(all_sfs, axis=0)
    all_sfs = np.expand_dims(all_sfs, axis=-1)
    all_responses = np.stack(all_responses)
    
    
    return(all_sfs, all_responses)


def plot_sfs(simulated_sfs, args):
    print("Saving exemplar SFS to sfs_machinelearning.png")
    print("=" * 80)
    sfs_div = simulated_sfs[0, :, :, 0]
    sfs_mig = simulated_sfs[args.n_reps, :, :, 0]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    axes[0].imshow(sfs_div, origin="lower")
    axes[0].set_title("Divergence (no migration)")
    axes[0].set_xlabel("Pop B")
    axes[0].set_ylabel("Pop A")

    axes[1].imshow(sfs_mig, origin="lower")
    axes[1].set_title("Gene flow (migration)")
    axes[1].set_xlabel("Pop B")
    axes[1].set_ylabel("Pop A")

    plt.tight_layout()
    plt.savefig('sfs_machinelearning.png')

def build_model(simulated_sfs, n_layers, dropout_rate, learning_rate):

    # create convolutional feature extractor
    conv1 = layers.Conv2D(10, (3, 3), activation='relu', input_shape=simulated_sfs.shape[1:])
    pool1 = layers.MaxPooling2D((2, 2))
    conv2 = layers.Conv2D(10, (3, 3), activation='relu')
    pool2 = layers.MaxPooling2D((2, 2))
    flatten = layers.Flatten(name="flatten")

    # specify input
    x = layers.Input(shape=simulated_sfs.shape[1:])

    # feature extraction
    x1 = conv1(x)
    x1 = pool1(x1)
    x1 = conv2(x1)
    x1 = pool2(x1)
    x1 = flatten(x1)

    # fully connected layers based on user args
    for layer_index in range(n_layers):
        hidden_units = 64 // (2**layer_index)
        x1 = layers.Dense(hidden_units, activation='relu', name=f"dense_{layer_index+1}")(x1)
        if dropout_rate > 0:
            x1 = layers.Dropout(dropout_rate, name=f"dropout_{layer_index+1}")(x1)

    outputs = layers.Dense(2, activation='softmax', name="final")(x1)

    # compile the model
    model = models.Model(inputs=x, outputs=outputs)
    model.compile(
        optimizer=optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=['accuracy'],
    )

    model.summary()

    return model


def main():

    args = parse_args()
    if args.layers < 1 or args.layers > 4:
        raise ValueError("--layers must be between 1 and 4.")
    if args.dropout < 0 or args.dropout > 1:
        raise ValueError("--dropout must be between 0.0 and 1.0.")

    if args.simulate:
        tdiv_prior=[50000, 500000] # prior on divergence time
        ne_prior=[10000, 100000] # prior on ne
        migrate_prior=[1e-6,1e-4] # prior on migration rate
        mu = 1e-7 # mutation rate
        rec_rate = 1e-8
        seq_len = 100_000 # sequence length
        replicates = 100 # nubmer of replicates to simulate per model (there are 5000 per model in the dataset we will load.)
        sample_size = 10 # number of individuals to sample per extant population

        simulated_sfs, simulated_responses = simulate_data(tdiv_prior, ne_prior, migrate_prior, sample_size, seq_len, mu, rec_rate, replicates)

        plot_sfs(simulated_sfs, args)

    if args.train:

        print("=" * 80)
        print("Training a CNN")
        print(f"  layers: {args.layers}")
        print(f"  dropout: {args.dropout}")
        print(f"  epochs: {args.epochs}")
        print(f"  learning rate: {args.learning_rate}")
        print("=" * 80)

        # load larger simulated dataset
        simulated_sfs = np.load("simulated_sfs.npy")
        simulated_responses = np.load("simulated_responses.npy")

        # divide data into training, test, and validation
        train_features, test_val_features, train_labels, test_val_labels = train_test_split(simulated_sfs, simulated_responses, test_size = 0.4, random_state=1234)
        test_features, val_features, test_labels, val_labels = train_test_split(test_val_features, test_val_labels, test_size = 0.2, random_state=1234)

        # save my testing dataset for later
        np.save('test_features.npy', test_features)
        np.save('test_labels.npy', test_labels)

        # convert labels to categorical
        train_labels_cat = to_categorical(train_labels, num_classes=2)
        test_labels_cat = to_categorical(test_labels, num_classes=2)
        val_labels_cat = to_categorical(val_labels, num_classes=2)

        # build the model
        model = build_model(simulated_sfs, args.layers, args.dropout, args.learning_rate)

        # fit our model
        history = model.fit(train_features, train_labels_cat, epochs=args.epochs, 
                                validation_data=(val_features, val_labels_cat), batch_size=args.batch_size)
        
        # save the model
        model.save('trained_model.h5')
    
    if args.test:
        print("=" * 80)
        print("Testing your CNN")
        print("=" * 80)

        # load test data
        test_features = np.load("test_features.npy")
        test_responses = np.load("test_labels.npy")

        # load model
        model = models.load_model('trained_model.h5')

        predict = model.predict(test_features)
        predicted_labels = np.argmax(predict, axis=1)
        matrix = confusion_matrix(test_responses, predicted_labels)
        accuracy = accuracy_score(test_responses, predicted_labels)
        
        print("=" * 80)
        print("Confusion Matrix:")
        print(matrix)
        print()
        print(f"Accuracy: {accuracy:.4f}")
        print("=" * 80)




if __name__ == "__main__":
    main()
