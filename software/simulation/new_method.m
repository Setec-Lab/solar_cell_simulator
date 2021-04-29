Voc = 2*2.690;
Vmp = 2*2.409;
Imp = 3*0.5029;
Isc = 3*0.5196;



I = linspace(Isc,0,1000)
factor = 1.005
for i = 1:1000
    if I(i) >= factor*Imp
        V(i) = ((Isc-I(i))/(Isc-Imp))*Vmp;
    else
        V(i) = Voc + (Vmp-Voc)*exp(-(abs(I(i)-Isc) - (Isc-factor*Imp))/(Imp/50));
    end
end
figure
plot(V,I)
        
% I = linspace(Isc,0,1000)
% factor = 1.005
% for i = 1:1000
%     if I(i) >= factor*Imp
%         V(i) = ((Isc-I(i))/(Isc-Imp))*Vmp;
%     else
%         V(i) = 0.95*Voc + (V(i-1)-0.95*Voc)*exp(-(abs(I(i)-Isc) - (Isc-factor*Imp))/(Imp/1));
%     end
% end
% figure
% plot(V,I)