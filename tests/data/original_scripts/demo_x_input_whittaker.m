
% Demonstration NMR spectrum smoothing with Whittaker smoother
% Optimal smoothing by cross-validation
%
% Paul Eilers, 2003

% Get the data
data = load('nmr_with_weights_and_x.csv');
x = data(: ,1);
y = data(:,2);



[z_order_2, ~] = whitsmdd(x, y, 2e4, 2);

writematrix(z_order_2,'output_x_and_y_2e4_2.csv')

[z_order_3, ~] = whitsmdd(x, y, 2e4, 3);

writematrix(z_order_3,'output_x_and_y_2e4_3.csv')


% Plot data and smooth
subplot(1, 1, 1);
plot([z_order_2-10 y] )    % Downward shift for visibility
hold on;
plot([z_order_3-10 y] )
title('NMR spectrum and optimal smooth')
xlabel('Channel')
ylabel('Signal strength')






