% Script for the analisys and control of the synchronous Buck converter %

%s = tf('s'); Use when in need of writing in 's' terms directly

% Converter parameters (defined by the user)
L = 68E-6;                         % Inductor value
rL = 17E-3;                        % Inductor series resistence

C = 99E-6;                         % Capacitor Value
rC = 58.33E-3;                     % Capacitor ESR

Vg = 15;                           % Input Voltage


% Tansfer function parameters
Gvd0 = Vg;                         % Gain
wESR = 1/(rC*C);                   % Zero originated from rC ESR (equivalent series resistance)
w0 = 1/(sqrt(L*C));                % Resonant frequency
Q = (1/(rC + rL))*(sqrt(L/C));     % Q-factor

% Transfer function
numerator = [rC*C 1];
denominator = [1/(w0^2) 1/(Q*w0) 1];
buckSys = tf(numerator , denominator);

bode(buckSys)
%step(buckSys)
