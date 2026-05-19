#!/usr/bin/env Rscript
# =============================================================================
# MBL Workshop Name Tag Generator
# =============================================================================
# Generates a print-ready PDF with multiple name tags per page (multi-up).
#
# Layout: 2 columns x 3 rows = 6 name tags per sheet (portrait 8.5" x 11")
#   - FRONTS PDF: all fronts, 6 per page
#   - BACKS PDF:  matching backs, mirrored left-right per row for duplex printing
#   - COMBINED PDF: fronts page then backs page, ready for manual duplex
#
# CSV must have columns: first_name, last_name, affiliation, ip_address
#
# Usage (from terminal):
#   Rscript generate_nametags.R participants.csv [output_dir]
#
# =============================================================================

library(grid)

# ── Configuration ─────────────────────────────────────────────────────────────

WORKSHOP_NAME <- "MBL Workshop on Molecular Evolution 2026"

# Card dimensions (inches)
CARD_W <- 4
CARD_H <- 3

# Page dimensions (inches) — US Letter portrait
PAGE_W <- 8.5
PAGE_H <- 11

# Grid layout
N_COLS <- 2
N_ROWS <- 3
CARDS_PER_PAGE <- N_COLS * N_ROWS

# Margins: center the grid on the page
MARGIN_X <- (PAGE_W - N_COLS * CARD_W) / 2   # 0.25" each side
MARGIN_Y <- (PAGE_H - N_ROWS * CARD_H) / 2   # 1.0" top and bottom

# Colors
COL_HEADER    <- "grey30"
COL_FIRSTNAME <- "black"
COL_LASTNAME  <- "black"
COL_FOOTER    <- "grey40"
COL_RULE      <- "grey70"
COL_BACK_LABEL <- "grey50"
COL_IP        <- "black"
COL_CUTLINE   <- "grey80"   # dashed cut guides

# ── Helper: shrink font size until text fits within max_width ─────────────────

fit_fontsize <- function(text, fontfamily, fontface, start_size,
                         max_width_in, min_size = 6) {
  size <- start_size
  while (size >= min_size) {
    w <- convertWidth(
      stringWidth(text),
      "inches", valueOnly = TRUE
    )
    # stringWidth uses current gpar; set it first
    pushViewport(viewport(gp = gpar(fontfamily = fontfamily,
                                    fontface    = fontface,
                                    fontsize    = size)))
    w <- convertWidth(stringWidth(text), "inches", valueOnly = TRUE)
    popViewport()
    if (w <= max_width_in) break
    size <- size - 1
  }
  size
}

# ── Draw one name tag FRONT inside the current viewport ──────────────────────

draw_front <- function(first, last, affiliation) {

  inner_w <- CARD_W   # viewport is already card-sized (inches)
  inner_h <- CARD_H
  pad_x   <- 0.18     # horizontal text padding (inches)
  max_txt  <- inner_w - 2 * pad_x

  # Background
  grid.rect(gp = gpar(fill = "white", col = "white"))

  # ── Header ──
  hdr_size <- fit_fontsize(WORKSHOP_NAME, "Helvetica", "plain", 12, max_txt)
  grid.text(
    WORKSHOP_NAME,
    x = 0.5, y = unit(inner_h - 0.22, "inches"),
    just = "centre",
    gp = gpar(fontfamily = "Helvetica", fontface = "plain",
               fontsize = hdr_size, col = COL_HEADER)
  )

  # Rule under header
  rule_y_in <- inner_h - 0.36
  grid.lines(
    x = unit(c(pad_x, inner_w - pad_x), "inches"),
    y = unit(c(rule_y_in, rule_y_in), "inches"),
    gp = gpar(col = COL_RULE, lwd = 0.8)
  )

  # ── Footer ──
  ftr_size <- fit_fontsize(affiliation, "Helvetica", "plain", 12, max_txt)
  grid.text(
    affiliation,
    x = 0.5, y = unit(0.18, "inches"),
    just = "centre",
    gp = gpar(fontfamily = "Helvetica", fontface = "plain",
               fontsize = ftr_size, col = COL_FOOTER)
  )

  # Rule above footer
  ftr_rule_y <- 0.18 + 12/72 + 0.06   # footer baseline + approx font height + gap
  grid.lines(
    x = unit(c(pad_x, inner_w - pad_x), "inches"),
    y = unit(c(ftr_rule_y, ftr_rule_y), "inches"),
    gp = gpar(col = COL_RULE, lwd = 0.8)
  )

  # ── Name: centered in body between the two rules ──
  body_top <- rule_y_in
  body_bot <- ftr_rule_y
  body_mid <- (body_top + body_bot) / 2

  first_size <- fit_fontsize(first, "Helvetica", "bold", 42, max_txt)
  last_size  <- fit_fontsize(last,  "Helvetica", "plain", 36, max_txt)

  # Stack first + last; compute combined block height
  first_h <- first_size / 72          # approximate cap height in inches
  last_h  <- last_size  / 72
  gap     <- 0.06                     # gap between first and last name
  block_h <- first_h + gap + last_h

  first_y <- body_mid + block_h / 2 - first_h / 2
  last_y  <- first_y - first_h / 2 - gap - last_h / 2 - 0.02

  grid.text(
    first,
    x = 0.5, y = unit(first_y, "inches"),
    just = "centre",
    gp = gpar(fontfamily = "Helvetica", fontface = "bold",
               fontsize = first_size, col = COL_FIRSTNAME)
  )
  grid.text(
    last,
    x = 0.5, y = unit(last_y, "inches"),
    just = "centre",
    gp = gpar(fontfamily = "Helvetica", fontface = "plain",
               fontsize = last_size, col = COL_LASTNAME)
  )
}

# ── Draw one name tag BACK inside the current viewport ───────────────────────

draw_back <- function(ip_address) {
  inner_w <- CARD_W
  inner_h <- CARD_H

  grid.rect(gp = gpar(fill = "white", col = "white"))

  # Label at top
  grid.text(
    "Workshop Network",
    x = 0.5, y = unit(inner_h - 0.28, "inches"),
    just = "centre",
    gp = gpar(fontfamily = "Helvetica", fontface = "plain",
               fontsize = 12, col = COL_BACK_LABEL)
  )

  # IP address — large, centered
  ip_size <- fit_fontsize(ip_address, "Helvetica", "bold", 28,
                          inner_w - 0.36)
  grid.text(
    ip_address,
    x = 0.5, y = 0.5,
    just = "centre",
    gp = gpar(fontfamily = "Helvetica", fontface = "bold",
               fontsize = ip_size, col = COL_IP)
  )

  # "IP Address" label below
  grid.text(
    "IP Address",
    x = 0.5, y = unit(inner_h / 2 - 0.45, "inches"),
    just = "centre",
    gp = gpar(fontfamily = "Helvetica", fontface = "plain",
               fontsize = 10, col = COL_BACK_LABEL)
  )
}

# ── Draw cut guides on the full page ─────────────────────────────────────────

draw_cut_guides <- function() {
  # Vertical cuts
  for (col in 0:N_COLS) {
    x_in <- MARGIN_X + col * CARD_W
    grid.lines(
      x = unit(c(x_in, x_in), "inches"),
      y = unit(c(0, PAGE_H), "inches"),
      gp = gpar(col = COL_CUTLINE, lwd = 0.5, lty = "dashed")
    )
  }
  # Horizontal cuts
  for (row in 0:N_ROWS) {
    y_in <- MARGIN_Y + row * CARD_H
    grid.lines(
      x = unit(c(0, PAGE_W), "inches"),
      y = unit(c(y_in, y_in), "inches"),
      gp = gpar(col = COL_CUTLINE, lwd = 0.5, lty = "dashed")
    )
  }
}

# ── Lay out one sheet of cards ────────────────────────────────────────────────
# cards: list of functions that draw into the current card viewport
# mirror_cols: set TRUE for back pages so col order flips (duplex alignment)

draw_sheet <- function(cards, mirror_cols = FALSE) {
  draw_cut_guides()

  n <- length(cards)
  for (i in seq_len(n)) {
    # Card position in grid (row 1 = top)
    grid_row <- ceiling(i / N_COLS)          # 1-indexed from top
    grid_col <- if (mirror_cols) {
      N_COLS - ((i - 1) %% N_COLS)           # mirror within each row
    } else {
      ((i - 1) %% N_COLS) + 1
    }

    # Convert to inches from bottom-left of page
    x_in <- MARGIN_X + (grid_col - 1) * CARD_W
    y_in <- PAGE_H - MARGIN_Y - grid_row * CARD_H

    vp <- viewport(
      x      = unit(x_in, "inches"),
      y      = unit(y_in, "inches"),
      width  = unit(CARD_W, "inches"),
      height = unit(CARD_H, "inches"),
      just   = c("left", "bottom"),
      clip   = TRUE
    )
    pushViewport(vp)
    cards[[i]]()
    # Draw card border (thin, for cutting reference)
    grid.rect(gp = gpar(col = COL_CUTLINE, fill = NA, lwd = 0.5))
    popViewport()
  }
}

# ── Main function ─────────────────────────────────────────────────────────────

generate_nametags <- function(csv_path, output_dir = "nametags_output") {

  if (!file.exists(csv_path)) stop("CSV file not found: ", csv_path)
  dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

  participants <- read.csv(csv_path, stringsAsFactors = FALSE,
                           strip.white = TRUE)

  required_cols <- c("first_name", "last_name", "affiliation", "ip_address")
  missing <- setdiff(required_cols, names(participants))
  if (length(missing) > 0) {
    stop("CSV is missing columns: ", paste(missing, collapse = ", "))
  }

  n <- nrow(participants)
  cat(sprintf("Generating name tags for %d participants...\n", n))

  # Pad to a full multiple of CARDS_PER_PAGE with blank entries
  n_padded  <- ceiling(n / CARDS_PER_PAGE) * CARDS_PER_PAGE
  n_sheets  <- n_padded / CARDS_PER_PAGE

  blank_front <- function() grid.rect(gp = gpar(fill = "white", col = NA))
  blank_back  <- blank_front

  # Build lists of draw-function closures
  make_front <- function(first, last, affil) {
    force(first); force(last); force(affil)
    function() draw_front(first, last, affil)
  }
  make_back <- function(ip) {
    force(ip)
    function() draw_back(ip)
  }

  fronts <- vector("list", n_padded)
  backs  <- vector("list", n_padded)
  for (i in seq_len(n)) {
    fronts[[i]] <- make_front(participants$first_name[i],
                              participants$last_name[i],
                              participants$affiliation[i])
    backs[[i]]  <- make_back(participants$ip_address[i])
  }
  for (i in (n + 1):n_padded) {
    fronts[[i]] <- blank_front
    backs[[i]]  <- blank_back
  }

  # ── Output: combined PDF (front sheet, back sheet, front sheet, back sheet…)
  combined_path <- file.path(output_dir, "nametags_print.pdf")
  pdf(combined_path, width = PAGE_W, height = PAGE_H, paper = "special")

  for (s in seq_len(n_sheets)) {
    idx <- ((s - 1) * CARDS_PER_PAGE + 1):(s * CARDS_PER_PAGE)

    # Front sheet
    grid.newpage()
    draw_sheet(fronts[idx], mirror_cols = FALSE)

    # Back sheet — mirror columns so duplex-flip aligns correctly
    grid.newpage()
    draw_sheet(backs[idx], mirror_cols = TRUE)
  }

  dev.off()

  cat(sprintf("\n✓ Print-ready PDF: %s\n", combined_path))
  cat(sprintf("  %d sheets of fronts + %d sheets of backs\n", n_sheets, n_sheets))
  cat(sprintf("  6 name tags per sheet  |  %.0f total cards printed\n", n_padded * 1.0))
  cat("\nPrinting tip:\n")
  cat("  - Print double-sided, flip on SHORT edge\n")
  cat("  - Or print odd pages (fronts), re-feed, print even pages (backs)\n")
  cat("  - Cut along the dashed guides\n")
}


