; $Id: cor.pro,v 7.0 2016/04/27 marcel.carbillet$
;+
; NAME:
;    cor
;
; ROUTINE'S PURPOSE:
;    cor manages the simulation for the CORonagraph (COR) module,
;    that is:
;       1-call the module's initialisation routine cor_init at the first
;         iteration of the simulation project,
;       2-call the module's program routine cor_prog otherwise, managing
;         at the same time the possible time integration/delay.
;
; MODULE'S PURPOSE:
;   COR simulates different types of coronagraphs, namely the Roddier & Roddier,
;   the Lyot, and the 4 Quadrant Phase Mask. This is a first attempt.
;
; CATEGORY:
;    main module's routine
;
; CALLING SEQUENCE:
;    error = cor(inp_wfp_t, $ ; input structure
;                out_img_t, $ ; output structure
;                par,       $ ; parameter structure
;                INIT=init  ) ; initialisation data structure
;
; OUTPUT:
;    error: long scalar (error code, see !caos_error var in caos_init.pro).
;
; INPUTS:
;    inp_wfp_t: structure of type wfp_t.
;    par      : parameters structure.
;
; INCLUDED OUTPUTS:
;    out_img_t: structure of type img_t.
;
; KEYWORD PARAMETERS:
;    INIT: initialisation data structure.
;    TIME: time-evolution structure.
;
; COMMON BLOCKS:
;    common caos_block, tot_iter, this_iter
;
;    tot_iter   : total number of iteration during the simulation run.
;    this_iter  : current iteration number.
;
; SIDE EFFECTS:
;    none.
;
; RESTRICTIONS:
;    Among them:
;    -No noises (photon noise, RON, dark current noise) and no background
;    addition implemented for now.
;    -No anisoplanatic difference is simulated between the main star and the
;    companion (exactly the same wavefront in entrance of the coronagraph).
;
; CALLED NON-IDL FUNCTIONS:
;    none.
;
; ROUTINE MODIFICATION HISTORY:
;    routine written: september 2003,
;                     Marcel Carbillet (OAA) [marcel@arcetri.astro.it],
;                     Olivier Lardiere (OAA) [lardiere@arcetri.astro.it].
;    modifications  : april 2016,
;                     Marcel Carbillet (Lagrange) [marcel.carbillet@unice.fr]:
;                    -adapted to Soft. Pack. CAOS 7.0.
;
; MODULE MODIFICATION HISTORY:
;    module written : Marcel Carbillet (OAA) [marcel@arcetri.astro.it],
;                     Olivier Lardiere (OAA) [lardiere@arcetri.astro.it].
;    modifications  : for version 5.0,
;                     Marcel Carbillet (LUAN) [marcel.carbille@unice.fr]:
;                    -stupid one-value-vector IDL6+ bug corrected (in cor_prog: n_phot->n_phot[0]).
;                   : for version 7.0,
;                     Marcel Carbillet (Lagrange) [marcel.carbillet@unice.fr]:
;                    -adapted to Soft. Pack. CAOS 7.0.
;
;-
;
function cor, inp_wfp_t,  $ ; input structure
              out_img_t,  $ ; output structure
              par,        $ ; COR parameters structure
              INIT=init     ; COR initialization structure

; CAOS global common block
common caos_block, tot_iter, this_iter

; error code initialisation
error = !caos_error.ok

; module's actions
if (this_iter eq 0) then begin
   ; initialisation section
   error = cor_init(inp_wfp_t, out_img_t, par, INIT=init)
endif else begin
   ; run section
   error = cor_prog(inp_wfp_t, out_img_t, par, INIT=init)
endelse
;filename = '/Data/PythonProjects/cor.fits'
;writefits, filename, error

; back to calling program.
return, error
end
