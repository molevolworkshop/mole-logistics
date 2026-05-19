# Printing name tags

We need to have two csv files:
- `faculty.csv`
- `students.csv`
with four columns:
- `first_name`
- `last_name`
- `affiliation`
- `ip_address`

We get these files from the `all-vm-ips.sh` script in `virtual-machines/late-additions`. _Note: We do not know if Paul created this script by manually copying names after running `listIPs.sh`. He will confirm._

We then run the `script-nametags.Rmd` script which sources the functions in `generate_nametags.R`. This file creates two folders `faculty_nametags_output` and `students_nametags_output`, each with a PDF file `nametags_print.pdf` with the front and back of nametags. The nametags already have the IP address in the back. PDFs need to be printed as "Flip on short edge" (sometimes called "landscape duplex" or "tumble") so that IP addresses are correctly mapped to names.

# Older information on nametags (pre May 2026) -- can be ignored!

## Message from Paul Lewis in slack
The labels in Scribus are 4 inches wide by 3 inches high. I got 4 labels per page in landscape orientation. The last name is in 42-point font and the first name (below the last name) is in 36 point font. At the top is a header that says "MBL Workshop on Molecular Evolution 2026" (12 point font) and on the bottom is a footer (12 point font) that has the name of the institution of the participant. I think I have an old Adobe InDesign template; if you use Adobe, let me know.

## Email from Paul Lewis (April 29, 2026)

Hi Claudia,

> We were wondering if you printed the name tags before getting to MBL or if you printed them there. 

I printed them before coming to Woods Hole. I've attached the Scribus (https://sourceforge.net/projects/scribus/) file (badges-2025-sla) I used last year to print the labels. Not very automated, I'm afraid. I just typed in the names and affiliations and printed them on colored cardstock I bought at the local Staples.

I've also attached my Adobe InDesign template (iplabels.indd) for printing the IP addresses that were stuck to the labels. You may want to avoid this hassle by just creating a printout of the IP addresses (once we have them after creating the virtual machines) and having the students copy their IP address from that.

In case you do want to use the InDesign template, you can just take a list of IP addresses and copy them into the template - no need to enter each IP address individually. I printed on  Staples label size 1/2" x 1 3/4" labels.

> Also, do you know by any chance where the nametag holders were stored?

I think Tracy collected the holders last year and stowed them perhaps with Maia in Maia's office in Loeb? You should check with Tracy to see if she remembers better.

-Paul