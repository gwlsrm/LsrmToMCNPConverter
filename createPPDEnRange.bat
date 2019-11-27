rem create in-files
python d:\gw\MyProgs\Python\MCNP\mcnpvarchanger.py PPD_in PPDinX5 ERG 0.05 E0 "0 0.001 0.0499 0.05"
python d:\gw\MyProgs\Python\MCNP\mcnpvarchanger.py PPD_in PPDin01 ERG 0.1 E0 "0 0.001 0.099 0.1"
python d:\gw\MyProgs\Python\MCNP\mcnpvarchanger.py PPD_in PPDin03 ERG 0.3 E0 "0 0.001 0.299 0.3"
python d:\gw\MyProgs\Python\MCNP\mcnpvarchanger.py PPD_in PPDin06 ERG 0.6 E0 "0 0.001 0.599 0.6"
python d:\gw\MyProgs\Python\MCNP\mcnpvarchanger.py PPD_in PPDin1 ERG 1 E0 "0 0.001 0.999 1"
python d:\gw\MyProgs\Python\MCNP\mcnpvarchanger.py PPD_in PPDin15 ERG 1.5 E0 "0 0.001 1.499 1.5"
python d:\gw\MyProgs\Python\MCNP\mcnpvarchanger.py PPD_in PPDin2 ERG 2 E0 "0 0.001 1.999 2"
python d:\gw\MyProgs\Python\MCNP\mcnpvarchanger.py PPD_in PPDin3 ERG 3 E0 "0 0.001 2.999 3"

rem calculation MCNP
mcnp5 n=PPD_in
del PPD_inr

mcnp5 n=PPDinX5
del PPDinX5r

mcnp5 n=PPDin01
del PPDin01r

mcnp5 n=PPDin03
del PPDin03r

mcnp5 n=PPDin06
del PPDin06r

mcnp5 n=PPDin1
del PPDin1r

mcnp5 n=PPDin15
del PPDin15r

mcnp5 n=PPDin2
del PPDin2r

mcnp5 n=PPDin3
del PPDin3r
