icurve = Icurve.signals.values;
vcurve = Vcurve.signals.values;
imodel = Imodel.signals.values;
vmodel = Vmodel.signals.values;
figure
hold on
plot(vcurve,icurve)
plot(vmodel,imodel)
legend('Equation', 'Real')
hold off
data_size = size(icurve);
MAE = 0;
for i = 1:data_size(1)
    MAE = MAE + abs(imodel(i) - icurve(i));
end
MAE = (MAE / data_size(1))