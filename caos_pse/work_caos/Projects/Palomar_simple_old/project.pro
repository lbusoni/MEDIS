;FILEVER:        8
;PROJECT: Palomar_simple
;       0 - PROJECT TYPE
;         100 - ITERATIONS
;      13 - NMODS
;       0       7       0       3 - Box
; MODULE: atm
;      16 - ID
;       1 - STATUS
;       0       0 - SLOT
;       0 - Ninputs
;       1 - Noutputs
;       0 - Output   Dtype:       1
; MODULE: cor
;      15 - ID
;       1 - STATUS
;       3       3 - SLOT
;       1 - Ninputs
;       4       1 - Input       0    Nptns:           2   Dtype:       6
;	     210     442
;	     230     335
;       1 - Noutputs
;       0 - Output   Dtype:       3
; MODULE: src
;       2 - ID
;       1 - STATUS
;       0       1 - SLOT
;       0 - Ninputs
;       1 - Noutputs
;       0 - Output   Dtype:       5
; MODULE: gpr
;       3 - ID
;       1 - STATUS
;       1       1 - SLOT
;       2 - Ninputs
;       2       0 - Input       0    Nptns:           2   Dtype:       5
;	      70     435
;	      90     427
;      16       0 - Input       1    Nptns:           2   Dtype:       1
;	      70     485
;	      90     442
;       1 - Noutputs
;       0 - Output   Dtype:       6
; MODULE: dmi
;       4 - ID
;       1 - STATUS
;       2       1 - SLOT
;       2 - Ninputs
;       3       0 - Input       0    Nptns:           2   Dtype:       6
;	     140     435
;	     160     427
;       9       0 - Input       1    Nptns:           4   Dtype:       8
;	     560     435
;	     570     460
;	     155     465
;	     160     442
;       2 - Noutputs
;       0 - Output   Dtype:       6
;       1 - Output   Dtype:       6
; MODULE: sws
;       5 - ID
;       1 - STATUS
;       3       1 - SLOT
;       1 - Ninputs
;       4       1 - Input       0    Nptns:           2   Dtype:       6
;	     210     442
;	     230     435
;       1 - Noutputs
;       0 - Output   Dtype:       4
; MODULE: bqc
;       6 - ID
;       1 - STATUS
;       4       1 - SLOT
;       1 - Ninputs
;       5       0 - Input       0    Nptns:           2   Dtype:       4
;	     280     435
;	     300     435
;       1 - Noutputs
;       0 - Output   Dtype:       7
; MODULE: rec
;       7 - ID
;       1 - STATUS
;       5       1 - SLOT
;       1 - Ninputs
;       6       0 - Input       0    Nptns:           2   Dtype:       7
;	     350     435
;	     370     435
;       1 - Noutputs
;       0 - Output   Dtype:       8
; MODULE: tfl
;       8 - ID
;       1 - STATUS
;       6       1 - SLOT
;       1 - Ninputs
;       7       0 - Input       0    Nptns:           2   Dtype:       8
;	     420     435
;	     440     435
;       1 - Noutputs
;       0 - Output   Dtype:       8
; MODULE: s*s
;       9 - ID
;       0 - STATUS
;       7       1 - SLOT
;       1 - Ninputs
;       8       0 - Input       0    Nptns:           2   Dtype:       8
;	     490     435
;	     510     435
;       1 - Noutputs
;       0 - Output   Dtype:       8
; MODULE: img
;      10 - ID
;       1 - STATUS
;       3       2 - SLOT
;       1 - Ninputs
;       4       1 - Input       0    Nptns:           2   Dtype:       6
;	     210     442
;	     230     385
;       2 - Noutputs
;       0 - Output   Dtype:       3
;       1 - Output   Dtype:       3
; MODULE: dis
;      12 - ID
;       1 - STATUS
;       4       2 - SLOT
;       1 - Ninputs
;      10       1 - Input       0    Nptns:           2   Dtype:       3
;	     280     392
;	     300     385
;       0 - Noutputs
; MODULE: dis
;      13 - ID
;       1 - STATUS
;       4       3 - SLOT
;       1 - Ninputs
;      15       0 - Input       0    Nptns:           2   Dtype:       3
;	     280     335
;	     300     335
;       0 - Noutputs
; --
; -- CAOS Application builder. Version 7.0
; --
; -- file: project.pro
; --
; -- Main procedure file for project: 
;  Projects/Palomar_simple
; -- Automatically generated on: Tue Apr 18 11:34:47 2017
; --
;

;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Error message procedure ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;

PRO ProjectMsg, TheMod
;              Common Block definition
;              =======================
;                  Total nmb Current  
;                  of iter.  iteration
;                  --------  ---------
COMMON caos_block, tot_iter, this_iter

MESSAGE,"Error calling Module: "+TheMod+" at iteration:"+STRING(this_iter)
END

COMMON caos_block, tot_iter, this_iter

tot_iter =          100
this_iter = 0
;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Load Parameter variables ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; - Module: atm_00016
atm_00016_c=0
RESTORE, 'Projects/Palomar_simple/atm_00016.sav'
atm_00016_p=par
; - Module: src_00002
src_00002_c=0
RESTORE, 'Projects/Palomar_simple/src_00002.sav'
src_00002_p=par
; - Module: s*s_00009
; - Module: gpr_00003
gpr_00003_c=0
RESTORE, 'Projects/Palomar_simple/gpr_00003.sav'
gpr_00003_p=par
; - Module: dmi_00004
dmi_00004_c=0
dmi_00004_t=0
RESTORE, 'Projects/Palomar_simple/dmi_00004.sav'
dmi_00004_p=par
; - Module: cor_00015
cor_00015_c=0
RESTORE, 'Projects/Palomar_simple/cor_00015.sav'
cor_00015_p=par
; - Module: sws_00005
sws_00005_c=0
sws_00005_t=0
RESTORE, 'Projects/Palomar_simple/sws_00005.sav'
sws_00005_p=par
; - Module: img_00010
img_00010_c=0
img_00010_t=0
RESTORE, 'Projects/Palomar_simple/img_00010.sav'
img_00010_p=par
; - Module: bqc_00006
bqc_00006_c=0
RESTORE, 'Projects/Palomar_simple/bqc_00006.sav'
bqc_00006_p=par
; - Module: rec_00007
rec_00007_c=0
RESTORE, 'Projects/Palomar_simple/rec_00007.sav'
rec_00007_p=par
; - Module: tfl_00008
tfl_00008_c=0
RESTORE, 'Projects/Palomar_simple/tfl_00008.sav'
tfl_00008_p=par
; - Module: dis_00012
dis_00012_c=0
RESTORE, 'Projects/Palomar_simple/dis_00012.sav'
dis_00012_p=par
; - Module: dis_00013
dis_00013_c=0
RESTORE, 'Projects/Palomar_simple/dis_00013.sav'
dis_00013_p=par

;;;;;;;;;;;;;;;;;
; Initialization;
;;;;;;;;;;;;;;;;;

t0=systime(/SEC)
print, " "
print, "=== RUNNING INITIALIZATION... ==="
@Projects/Palomar_simple/mod_calls.pro
ti=systime(/SEC)-t0

;;;;;;;;;;;;;;;;
; Loop Control ;
;;;;;;;;;;;;;;;;

t0=systime(/SEC)
print, " "
print, "=== RUNNING SIMULATION...     ==="
FOR this_iter=1L, tot_iter DO BEGIN		; Begin Main Loop
	print, "=== ITER. #"+strtrim(this_iter)+"/"+$
         strtrim(tot_iter,1)+"...", FORMAT="(A,$)"
  if this_iter LT tot_iter then begin
     for k=0,79 do print, string(8B), format="(A,$)"
  endif else print, " " 
	@Projects/Palomar_simple/mod_calls.pro
ENDFOR							; End Main Loop
ts=systime(/SEC)-t0
print, " "
print, "=== CPU time for initialization phase    =", ti, " s."
print, "=== CPU time for simulation phase        =", ts, " s."
print, "    [=> CPU time/iteration=", strtrim(ts/tot_iter,2), "s.]"
print, "=== total CPU time (init.+simu. phases)  =", ti+ts, " s."
print, " "
;;;;;;;;;;;;;;;;;
; End Main      ;
;;;;;;;;;;;;;;;;;

END
