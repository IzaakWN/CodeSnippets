/*****************************************************************************
 * Project: RooFit                                                           *
 *                                                                           *
  * This code was autogenerated by RooClassFactory                            * 
 *****************************************************************************/

#ifndef ROOCFAUTO000PDF
#define ROOCFAUTO000PDF

#include "RooAbsPdf.h"
#include "RooRealProxy.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
 
class RooCFAuto000Pdf : public RooAbsPdf {
public:
  RooCFAuto000Pdf() {} ; 
  RooCFAuto000Pdf(const char *name, const char *title,
	      RooAbsReal& _x,
	      RooAbsReal& _a);
  RooCFAuto000Pdf(const RooCFAuto000Pdf& other, const char* name=0) ;
  virtual TObject* clone(const char* newname) const { return new RooCFAuto000Pdf(*this,newname); }
  inline virtual ~RooCFAuto000Pdf() { }

protected:

  RooRealProxy x ;
  RooRealProxy a ;
  
  Double_t evaluate() const ;

private:

  ClassDef(RooCFAuto000Pdf,1) // Your description goes here...
};
 
#endif
