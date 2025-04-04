#include "datasets.h"

// Evaluate on the Google Transparency Report Dataset as described in
// Section 5.2 of https://arxiv.org/pdf/1712.01208
void transparency_report(struct model_state *s) {
  // Vary the following to see different results of the model. The current
  // values have been taken from Table 1 of our paper, in which we describe why
  // they are realistic and extracted from the experimental of Kraska et al.
  s->c = 0.25;
  s->n = 1700000;                 // 1.7M urls
  s->lambda = 128;                // 128 bits
  s->m_l = 1 * 1024 * 1024 * 8;   // 1 Megabyte
  s->m_a = 0.5 * 1024 * 1024 * 8; // 0.5 Megabytes
  s->m_b = s->m_a;
  s->q = 0.5;
}

void malicious_urls(struct model_state *s) {
  s->c = 0.25;
  s->n = 223088;
  s->lambda = 128;
  s->m_l = 1 * 1024 * 1024 * 8;   // 1 Megabyte
  s->m_a = 0.5 * 1024 * 1024 * 8; // 0.5 Megabytes
  s->m_b = s->m_a;
  s->q = 0.5;
}

void ember(struct model_state *s) {
  s->c = 0.25;
  s->n = 300000;
  s->lambda = 128;
  s->m_l = 1 * 1024 * 1024 * 8;   // 1 Megabyte
  s->m_a = 0.5 * 1024 * 1024 * 8; // 0.5 Megabytes
  s->m_b = s->m_a;
  s->q = 0.5;
}
