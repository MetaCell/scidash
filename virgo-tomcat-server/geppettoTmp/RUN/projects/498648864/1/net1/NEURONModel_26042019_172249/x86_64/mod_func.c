#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _RS_reg(void);
extern void _RS_Iext_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," RS.mod");
    fprintf(stderr," RS_Iext.mod");
    fprintf(stderr, "\n");
  }
  _RS_reg();
  _RS_Iext_reg();
}
