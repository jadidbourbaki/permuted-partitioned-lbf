#ifndef DATASET_H
#define DATASET_H

#include "model.h"

// Evaluate on the Google Transparency Report Dataset as described in
// Section 5.2 of https://arxiv.org/pdf/1712.01208
void transparency_report(struct model_state *s);

void malicious_urls(struct model_state *s);

void ember(struct model_state *s);

#endif // DATASET_H
