% Demonstration NMR spectrum smoothing with Whittaker smoother
% Optimal smoothing by cross-validation
%
% Paul Eilers, 2003

% Get the data
data = load('nmr_with_weights_and_x.csv');
y = data(:,2);


[z_2, ~] = whitsm(y, 2e4, 2);

writematrix(z_2,'output_only_y_2e4_2.csv')

[z_3, ~] = whitsm(y, 2e4,3);

writematrix(z_3,'output_only_y_2e4_3.csv')

% Plot data and smooth
subplot(1, 1, 1);
plot([z_2-10 y] )    % Downward shift for visibility
hold on;
plot([z_3-10 y] ) 
title('NMR spectrum and optimal smooth')
xlabel('Channel')
ylabel('Signal strength')



