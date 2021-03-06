;FILEVER:        8
;PROJECT: SHCalibration
;       0 - PROJECT TYPE
;          44 - ITERATIONS
;       9 - NMODS
;       0       4       0       2 - Box
; MODULE: mds
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
; MODULE: sws
;       4 - ID
;       1 - STATUS
;       2       1 - SLOT
;       1 - Ninputs
;       3       0 - Input       0    Nptns:           2   Dtype:       6
;	     140     435
;	     160     435
;       1 - Noutputs
;       0 - Output   Dtype:       4
; MODULE: bqc
;       5 - ID
;       1 - STATUS
;       3       1 - SLOT
;       1 - Ninputs
;       4       0 - Input       0    Nptns:           2   Dtype:       4
;	     210     435
;	     230     435
;       1 - Noutputs
;       0 - Output   Dtype:       7
; MODULE: scd
;       7 - ID
;       1 - STATUS
;       4       0 - SLOT
;       2 - Ninputs
;       5       0 - Input       0    Nptns:           2   Dtype:       7
;	     280     435
;	     300     477
;       1       0 - Input       1    Nptns:           3   Dtype:       1
;	      70     485
;	     280     485
;	     300     492
;       0 - Noutputs
; MODULE: dis
;       8 - ID
;       1 - STATUS
;       2       2 - SLOT
;       1 - Ninputs
;       3       0 - Input       0    Nptns:           2   Dtype:       6
;	     140     435
;	     160     385
;       0 - Noutputs
; MODULE: dis
;       9 - ID
;       1 - STATUS
;       3       2 - SLOT
;       1 - Ninputs
;       4       0 - Input       0    Nptns:           2   Dtype:       4
;	     210     435
;	     230     385
;       0 - Noutputs
; MODULE: dis
;      10 - ID
;       1 - STATUS
;       4       1 - SLOT
;       1 - Ninputs
;       5       0 - Input       0    Nptns:           2   Dtype:       7
;	     280     435
;	     300     435
;       0 - Noutputs
;
;TEXT: mirror deformations
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;        2     501  - Location
;
;TEXT: interaction matrix
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;      279     502  - Location
;
;TEXT: SH wavefront sensor
;        0  - Angle
;    0   0   0  - Color
; Courier*italic  - Fontname
;       14.0000  - Size
;      129     454  - Location
; --
; -- CAOS Application builder. Version 7.0
; --
; -- file: project.pro
; --
; -- Main procedure file for project: 
;  Projects/SHCalibration
; -- Automatically generated on: Sun Jun 19 18:16:50 2016
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

tot_iter =           44
this_iter = 0
;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Load Parameter variables ;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; - Module: mds_00001
mds_00001_c=0
RESTORE, 'Projects/SHCalibration/mds_00001.sav'
mds_00001_p=par
; - Module: src_00002
src_00002_c=0
RESTORE, 'Projects/SHCalibration/src_00002.sav'
src_00002_p=par
; - Module: gpr_00003
gpr_00003_c=0
RESTORE, 'Projects/SHCalibration/gpr_00003.sav'
gpr_00003_p=par
; - Module: sws_00004
sws_00004_c=0
sws_00004_t=0
RESTORE, 'Projects/SHCalibration/sws_00004.sav'
sws_00004_p=par
; - Module: bqc_00005
bqc_00005_c=0
RESTORE, 'Projects/SHCalibration/bqc_00005.sav'
bqc_00005_p=par
; - Module: scd_00007
scd_00007_c=0
RESTORE, 'Projects/SHCalibration/scd_00007.sav'
scd_00007_p=par
; - Module: dis_00008
dis_00008_c=0
RESTORE, 'Projects/SHCalibration/dis_00008.sav'
dis_00008_p=par
; - Module: dis_00009
dis_00009_c=0
RESTORE, 'Projects/SHCalibration/dis_00009.sav'
dis_00009_p=par
; - Module: dis_00010
dis_00010_c=0
RESTORE, 'Projects/SHCalibration/dis_00010.sav'
dis_00010_p=par

;;;;;;;;;;;;;;;;;
; Initialization;
;;;;;;;;;;;;;;;;;

t0=systime(/SEC)
print, " "
print, "=== RUNNING INITIALIZATION... ==="
@Projects/SHCalibration/mod_calls.pro
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
	@Projects/SHCalibration/mod_calls.pro
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
