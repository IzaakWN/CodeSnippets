// ~seligman/root-class/ExampleEvent.h
// 21-May-2009 <seligman@nevis.columbia.edu>

// This class was created as part of Bill Seligman's two-day ROOT
// tutorial in 2009.  It mimics the kind of information that one might
// find in a typical physics-event class.  In a real experiment, the
// data structures would be much more complex.

#ifndef ROOTTutorial_ExampleEvent_h
#define ROOTTutorial_ExampleEvent_h

#include <TObject.h>
#include <Rtypes.h>

#include <vector>
#include <cmath>


// An extremely simplistic definition of particle information.
class ExampleParticle : public TObject
{
public:
  ExampleParticle() {};
  virtual ~ExampleParticle() {};
public:
  Double_t px;
  Double_t py;
  Double_t pz;
  Int_t pdg;
  ClassDef(ExampleParticle,1);  // Example group of information for a single particle.
};


// A slightly more complex definition of a detector event.
class ExampleEvent : public TObject
{
public:

  // Class constructor
  ExampleEvent( Int_t run = 0, Int_t event = 0 );

  // Class destructor
  virtual ~ExampleEvent();

  // The run number for this event.
  Int_t GetRun() const { return m_run; }

  // The event number within the run.
  Int_t GetEvent() const { return m_event; }

  // The numbers of different types of particles identified in the event.
  Int_t GetNumberLeptons() const { return m_leptons.size(); }
  Int_t GetNumberPhotons() const { return m_photons.size(); }
  Int_t GetNumberHadrons() const { return m_hadrons.size(); }

  // Accessor methods for the different particle types; e.g., the
  // following method returns px for the i-th lepton.  Note that there
  // are no checks to see if you've asked for information on more
  // particles than exist in the event!

  Double_t LeptonPx( const Int_t i ) const { return m_leptons[i].px; }
  Double_t LeptonPy( const Int_t i ) const { return m_leptons[i].py; }
  Double_t LeptonPz( const Int_t i ) const { return m_leptons[i].pz; }
  // PDG = "particle data group", which has assigned ID codes to every
  // type of known or theorized particle.
  Int_t LeptonPDG( const Int_t i ) const { return m_leptons[i].pdg; }

  Double_t PhotonPx( const Int_t i ) const { return m_photons[i].px; }
  Double_t PhotonPy( const Int_t i ) const { return m_photons[i].py; }
  Double_t PhotonPz( const Int_t i ) const { return m_photons[i].pz; }
  // PDG = "particle data group", which has assigned ID codes to every
  // type of known or theorized particle.
  Int_t PhotonPDG( const Int_t i ) const { return m_photons[i].pdg; }

  Double_t HadronPx( const Int_t i ) const { return m_hadrons[i].px; }
  Double_t HadronPy( const Int_t i ) const { return m_hadrons[i].py; }
  Double_t HadronPz( const Int_t i ) const { return m_hadrons[i].pz; }
  // PDG = "particle data group", which has assigned ID codes to every
  // type of known or theorized particle.
  Int_t HadronPDG( const Int_t i ) const { return m_hadrons[i].pdg; }

  // The Build method erases any existing content of this class and
  // creates "dummy" data for the purpose of the tutorial.  In a real
  // experiment, such a method would not exist.
  void Build();

private:

  Int_t m_run; // Run number
  Int_t m_event; // Event number

  typedef std::vector< ExampleParticle >  m_list_type;
  typedef m_list_type::iterator           iterator;

  m_list_type m_leptons; // the leptons associated with this event.
  m_list_type m_photons; // the photons associated with this event.
  m_list_type m_hadrons; // the photons associated with this event.

public:
  // The following is a macro defined in TObject.h.  The second number
  // is the "version number" of this class definition; if we change
  // the class, we should increment the version number.  This allows
  // ROOT to read files created with several different versions of a
  // class (very handy for reading old files during the course of an
  // experiment's analysis!).
  ClassDef(ExampleEvent,1);  // Example event for ROOT tutorial
};

#endif // ROOTTutorial_ExampleEvent_h
