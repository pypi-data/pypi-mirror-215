# Examples

## start_here.ipynb

describes workflow + data format

## paper_visualization.ipynb

contains miscellaneous visualization from the paper.

### Data

`data/ex{i}.txt` - synthetic data for basic visualization

## paper_example_1.ipynb

Source: https://data.nist.gov/od/id/mds2-2418
Note: we used the following bash script to preprocess the data in CM1, CM2, CM3, and Isomers.

```bash
for n in *; do
awk -F, '/^#/ {print $0}; /^[^#]/ {print $2, $3}' < $n > $n.txt
done
```

Here is the notebook which explains example 1: `paper_example1.ipynb`.

### Data

CM1, CM2, CM3, were from https://data.nist.gov/od/id/mds2-2418/pdr:v/1.0.1.

<details>
<summary>
Names and formulas for all compounds in `data/`
</summary>
<code>
CM1,01,Acetyl norfentanyl,C13H18N2O,
CM1,02,Remifentanil,C20H28N2O5,
CM1,03,Acrylfentanyl,C22H26N2O,
CM1,04,p-Fluorobutyryl Fentanyl,C23H29FN2O,
CM1,05,Cyclopentyl Fentanyl,C25H32N2O,
CM1,06,3-Furanyl fentanyl,C24H26N2O2,
CM1,07,4-ANPP,C19H24N2,
CM1,08,U-49900,C18H26Cl2N2O,
CM1,09,Acetyl fentanyl,C21H26N2O,
CM1,10,4'-methyl Acetyl Fentanyl,C22H28N2O,
CM1,11,Carfentanil,C24H30N2O3,
CM1,12,p-Methoxyfentanyl,C23H30N2O2,
CM1,13,U-47700,C16H22Cl2N2O,
CM1,14,FIBF,C23H29FN2O,
CM1,15,p-Fluorofentanyl,C22H27FN2O,
CM1,16,Crotonyl Fentanyl,C23H28N2O,
CM1,17,Tetrahydrofuran Fentanyl ,C24H30N2O2,
CM1,18,U-48800,C17H24Cl2N2O,
CM1,19,trans-3-methyl Fentanyl,C23H30N2O,
CM1,20,Butyryl Fentanyl,C23H30N2O,
CM1,21,Valeryl Fentanyl,C24H32N2O,
CM1,22,_-Hydroxythiofentanyl,C20H26N2O2S,
CM1,23,Benzyl Fentanyl,C21H26N2O,
CM1,24,cis-3-methyl Fentanyl,C23N30N2O,
CM1,25,Cyclopropyl Fentanyl,C23H28N2O,
CM1,26,Methoxyacetyl Fentanyl,C22H28N2O2,
CM1,27,2-Furanyl fentanyl  ,C24H26N2O2,
CM1,28,Fentanyl,C22H28N2O,
CM2,01,N-Ethylbuphedrone,C12H17NO,
CM2,02,3-Ethylmethcathinone,C12H17NO,
CM2,03,4-Chloroethcathinone,C11H14ClNO,
CM2,04,"3,4-Methylenedioxy-N-isopropylcathinone",C13H17NO3,
CM2,05,Pentylone,C13H17NO3,
CM2,06,N-Butyl Pentylone,C16H23NO3,
CM2,07,3-Fluoromethcathinone,C10H12FN,
CM2,08,2-Ethylmethcathinone,C12H17NO,
CM2,09,"2,3-Dimethylmethcathinone",C12H17NO,
CM2,10,3-Chloroethcathinone,C11H14ClNO,
CM2,11,"2,3-Ethylone isomer",C12H15NO3,
CM2,12,"2,3-Pentylone",C13H17NO3,
CM2,13,"N,N-Dimethylpentylone",C14H19NO3,
CM2,14,2-Methyl-4'-(methylthio)-2-Morpholinopropiophenone,C15H21NO2S,
CM2,15,"2-Chloro-N,N-dimethylcathinone",C11H14ClNO,
CM2,16,"3,4-Methylenedioxyamphetamine",C10H13NO2,
CM2,17,4-Methylbuphedrone,C12H17NO,
CM2,18,4-Chlorobuphedrone,C11H14ClNO,
CM2,19,Methylone,C11H13NO3,
CM2,20,"3',4'-Methylenedioxy-N-tert-butylcathinone",C14H19NO3,
CM2,21,N-Ethylpentylone,C14H19NO3,
CM2,22,Naphyrone,C19H23NO,
CM2,23,Cathinone,C9H11NO,
CM2,24,Pentedrone,C12H17NO,
CM2,25,2-Chloroethcathinone,C11H14ClNO,
CM2,26,"3,4-Dimethylmethcathinone",C12H17NO,
CM2,27,MMDMA,C12H17NO3,
CM2,28,"3,4-Methylenedioxy-alpha-methylamino-isovalerapheronone",C13H17NO3,
CM2,29,MPHP,C17H25NO,
CM2,30,Flephedrone,C10H12FNO,
CM2,31,"4-Methyl-N,N-dimethylcathinone",C12H17NO,
CM2,32,"3-Chloro-N,N-dimethylcathinone",C11H14ClNO,
CM2,33,MePPP,C14H19NO,
CM2,34,"N,N-diethylpentylone",C16H23NO3,
CM2,35,p-Methoxyamphetamine,C10H15NO,
CM2,36,3-Methylbuphedrone,C12H17NO,
CM2,37,"3,4-Methylenedioxymethamphetamine",C22H15NO2,
CM2,38,Methedrone,C11H15NO2,
CM2,39,Ethylone,C12H15NO3,
CM2,40,Benzphetamine,C17H21N,
CM2,41,N-sec-butyl Pentylone,C16H23NO3,
CM2,43,"2,4-Dimethylmethcathinone",C12H17NO,
CM2,44,"4-Chloro-N,N-dimethylcathinone",C11H14ClNO,
CM2,45,N-Ethyl Hexedrone,C14H21NO,
CM2,46,_-PVP,C15H21NO,
CM2,47,_-Pyrrolidinohexanophenone,C16H23NO,
CM2,48,N-isobuytl Pentylone,C16H23NO3,
CM2,49,4-Methylmethcathinone,C11H15NO,
CM2,50,4-Chloromethcathinone,C10H12ClNO,
CM2,51,4-Ethylmethcathinone,C12H17NO,
CM2,52,4-Methyl-_-ethylaminopentiophenone,C14H21NO,
CM2,53,Butylone,C12H15NO3,
CM2,54,"3,4-Methylenedioxy-N-propylcathinone",C13H17NO3,
CM2,55,N-propyl Hexylone,C16H23NO3,
CM2,56,_-PBP,C15H21NO,
CM2,57,Dibutylone,C13H17NO3,
CM2,58,Eutylone,C13H17NO3,
CM2,59,3-Methylethecathinone,C12H17NO,
CM3,01,_-8-Tetrahydrocannabinol,C21H30O2,
CM3,02,UR-144,C21H29NO,
CM3,03,5-Fluoro-AMB,C19H26FN3O3,
CM3,04,JWH-302,C22H25NO2,
CM3,05,JWH-073,C23H21NO,
CM3,06,5-Fluoro-AKB48,C20H30FN3O,
CM3,07,5-Fluoro ADBICA,C20H28FN3O2,
CM3,08,MAM2201,C25H24FNO,
CM3,09,2-Fluoro-ADB,C20H28FN3O3,
CM3,10,PX2,C22H25FN4O2,
CM3,11,EMB-FUBINACA,C22H24FN3O3,
CM3,12,MMB2201,C20H27FN2O3,
CM3,13,AB-CHMINACA,C20H28N4O2,
CM3,14,AB-FUBINACA isomer 1,C20H21FN4O2,
CM3,15,THJ,C22H22N4O,
CM3,16,NM2201,C24H22FNO2,
CM3,17,_-9-Tetrahydrocannabinol,C21H30O2,
CM3,18,3-Fluoro-ADB,C20H28FN3O3,
CM3,19,ADB-PINACA,C19H28N4O2,
CM3,20,JWH-203,C21H22ClNO,
CM3,21,5-Fluoro-MDMB-PICA,C21H29FN2O3,
CM3,22,THJ2201,C23H21FN2O,
CM3,23,AB-7-FUBAICA,C20H21FN4O2,
CM3,24,JWH-210,C26H27NO,
CM3,25,Cannabinol,C21H26O2,
CM3,26,XLR11,C21H28FNO,
CM3,27,MMB-FUBINACA,C21H22FN3O3,
CM3,28,JWH-250,C22H25NO2,
CM3,29,JWH-201,C22H25NO2,
CM3,30,MDMB-CHMICA,C23H32N2O3,
CM3,31,4-Cyano-CUMYL-BUTINACA,C22H24N4O,
CM3,32,"CP 47,497",C21H34O2,
CM3,33,4-Fluoro-ADB,C20H28FN3O3,
CM3,34,FUB-AMB,C21H22FN3O3,
CM3,35,AKB48,C23H31N3O,
CM3,36,AM2201 benzimidazole analog,C23H21FN2O,
CM3,37,AB-FUBINACA isomer 2,C20H21FN4O2,
CM3,38,JWH-122 N-(4-pentenyl) analog,C25H25NO,
CM3,39,5-Chloro-AKB48,C20H30ClN3O,
CM3,40,"CP 47,497-C8-homolog",C21H34O2,
CM3,41,AB-PINACA,C18H26N4O2,
CM3,42,AB-FUBINACA 2'-indazole isomer,C20H21FN4O2,
CM3,43,ADB-CHMINACA,C21H30N4O2,
CM3,44,AB-FUBINACA,C20H21FN4O2,
CM3,45,JWH-122,C25H25NO,
CM3,46,JWH-081,C25H25NO2,
CM3,47,APP-CHMINACA,C24H28N4O2,
CM3,48,FDU-PB-22,C26H18FNO2,
CM3,49,JWH-018,C24H23NO,
Isomers,01,3-Fluoromethamphetamine,C10H14FNO3,
Isomers,05,2-Fluoromethamphetamine,C10H14FN,
Isomers,06,Cannabichromene,C21H30O2,
Isomers,09,Phentermine,C10H15N,
Isomers,10,delta-8-THC,C21H30O2,
Isomers,12,LSD,C20H25N3O,
Isomers,13,Methamphetamine,C10H15N,
Isomers,14,delta-9-THC,C21H30O2,
Isomers,15,o-FBF,C23H29FN2O,

DART-MS:
1. Cotinine and 2. Serotonin
3. Phenibut and 4. MDA
5. MMDPPA and 6. Methylone
7. 5-methoxy MET and 8. Norfentanyl
9. Cocaine and 10. Scopolamine
11. HU-210 and 12. Testosterone Isocaprionate
13. Methamphetamine and 14. Phentermine. 
</code>
</details>

## paper_example_2.ipynb

TODO: describe this
