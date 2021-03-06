;FILEVER:        8
;PROJECT: MDIS2
;       0 - PROJECT TYPE
;          10 - ITERATIONS
;      13 - NMODS
;       0       7       0       5 - Box
; MODULE: dis
;      23 - ID
;       1 - STATUS
;       4       5 - SLOT
;       1 - Ninputs
;      22       0 - Input       0    Nptns:           2   Dtype:       3
;	     280     235
;	     300     235
;       0 - Noutputs
; MODULE: cor
;      22 - ID
;       1 - STATUS
;       3       5 - SLOT
;       1 - Ninputs
;       4       1 - Input       0    Nptns:           2   Dtype:       6
;	     210     442
;	     230     235
;       1 - Noutputs
;       0 - Output   Dtype:       3
; MODULE: atm
;       1 - ID
;       1 - STATUS
;       0       0 - SLOT
;       0 - Ninputs
;       1 - Noutputs
;       0 - Output   Dtype:       1
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
;       1       0 - Input       1    Nptns:           2   Dtype:       1
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
;       9       0 - Input       1    Nptns:           6   Dtype:       8
;	     560     435
;	     570     435
;	     570     460
;	     150     460
;	     150     450
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
;      16 - ID
;       1 - STATUS
;       3       0 - SLOT
;       1 - Ninputs
;       4       1 - Input       0    Nptns:           2   Dtype:       6
;	     210     442
;	     230     485
;       2 - Noutputs
;       0 - Output   Dtype:       3
;       1 - Output   Dtype:       3
; MODULE: dis
;      17 - ID
;       1 - STATUS
;       4       0 - SLOT
;       1 - Ninputs
;      16       1 - Input       0    Nptns:           2   Dtype:       3
;	     280     492
;	     300     485
;       0 - Noutputs
;
;TEXT: DM
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;      159     403  - Location
;
;TEXT: SH wfs
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;      227     404  - Location
;
;TEXT: wf rec.
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;      363     401  - Location
;
;TEXT: ctrl
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;      443     402  - Location
;
;TEXT: close the loop
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;      508     404  - Location
;
;TEXT: imaging
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;      211     502  - Location
;
;TEXT: turbulent atm.
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;        1     501  - Location
;
;TEXT: NGS
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;        4     402  - Location
;
;TEXT: telescope
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;       71     401  - Location
; --
; -- CAOS Application builder. Version 7.0
; --
; -- file: project.pro
; --
; -- Main procedure file for project: 
;  Projects/MDIS2
; -- Automatically generated on: Mon Apr 17 22:06:33 2017
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

tot_iter =           10
this_iter = 0
;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Load Parameter variables ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; - Module: atm_00001
atm_00001_c=0
RESTORE, 'Projects/MDIS2/atm_00001.sav'
atm_00001_p=par
; - Module: src_00002
src_00002_c=0
RESTORE, 'Projects/MDIS2/src_00002.sav'
src_00002_p=par
; - Module: s*s_00009
; - Module: gpr_00003
gpr_00003_c=0
RESTORE, 'Projects/MDIS2/gpr_00003.sav'
gpr_00003_p=par
; - Module: dmi_00004
dmi_00004_c=0
dmi_00004_t=0
RESTORE, 'Projects/MDIS2/dmi_00004.sav'
dmi_00004_p=par
; - Module: cor_00022
cor_00022_c=0
RESTORE, 'Projects/MDIS2/cor_00022.sav'
cor_00022_p=par
; - Module: sws_00005
sws_00005_c=0
sws_00005_t=0
RESTORE, 'Projects/MDIS2/sws_00005.sav'
sws_00005_p=par
; - Module: img_00016
img_00016_c=0
img_00016_t=0
RESTORE, 'Projects/MDIS2/img_00016.sav'
img_00016_p=par
; - Module: bqc_00006
bqc_00006_c=0
RESTORE, 'Projects/MDIS2/bqc_00006.sav'
bqc_00006_p=par
; - Module: rec_00007
rec_00007_c=0
RESTORE, 'Projects/MDIS2/rec_00007.sav'
rec_00007_p=par
; - Module: dis_00023
dis_00023_c=0
RESTORE, 'Projects/MDIS2/dis_00023.sav'
dis_00023_p=par
; - Module: tfl_00008
tfl_00008_c=0
RESTORE, 'Projects/MDIS2/tfl_00008.sav'
tfl_00008_p=par
; - Module: dis_00017
dis_00017_c=0
RESTORE, 'Projects/MDIS2/dis_00017.sav'
dis_00017_p=par

;;;;;;;;;;;;;;;;;
; Initialization;
;;;;;;;;;;;;;;;;;

t0=systime(/SEC)
print, " "
print, "=== RUNNING INITIALIZATION... ==="
@Projects/MDIS2/mod_calls.pro
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
	@Projects/MDIS2/mod_calls.pro
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
