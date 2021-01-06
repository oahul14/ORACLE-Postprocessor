# Calculating enhancement ratios.

According to previous studies (Wu et al., 2020; Lefer et al., 1994), the enhancement ratios (ER) of BC and OA is calculable if the excess concentration of CO is available, i.e.: 

$$ER = \frac{BC}{\Delta CO}$$

where $\Delta CO$ is the CO concentration with background CO concentration subtracted. During the calculation of BC and OA enhancement ratios, the background CO was determined by averaging CO concentrations when BC is less than $100\space ng/m^3$. After subtracting the background CO concentration, the ER was calculated by solving a linear orthogonal distance regression (LODR) as shown in the figure. The state-of-the-art ODRPACK, which was originally written in FORTRAN, was ustilised by calling scipy.odr, an efficiently parsed python package. 

The time series figure shows the beta slope with one standard error stated as errorbars. FT and BL were separatly calculated with an altitude of $1200m$ for all 6 days of observation$^1$.

The space series figure shows same slopes with errorbars but separated according to areas. The general slopes and standard errors in bottom, middle and upper area on all observation days were present$^2$.

$^1$: OA observations were only available on 0813, 0815, 0826 and 0828. On 0828, only less than 20 observations were valid for both CO and BC. Therefore, only results from 0813, 0815 and 0826 are present on the figure.
$^2$: BC and OA observations in the BL showed strong daily variation across the observation period, with large standard error of the same magitude of the slope.

