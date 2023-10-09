
% Demonstration NMR spectrum smoothing with Whittaker smoother
% Optimal smoothing by cross-validation
%
% Paul Eilers, 2003

% Get the data
data = load('nmr_with_weights_and_x.csv');
y = data(:,2);
evenly_space_weights = data(:,3);
random_weights = data(:, 4);


[z_even, ~] = whitsmw(y, evenly_space_weights, 2e4, 2);

writematrix(z_even,'output_y_with_weights_2e4_2.csv');

[z_random, ~] = whitsmw(y, random_weights, 2e4, 3);

writematrix(z_random,'output_y_with_random_weights_2e4_3.csv')


% Plot data and smooth
subplot(1, 1, 1);
plot([z_even-10 y] )    % Downward shift for visibility
hold on;
plot([z_random-10 y] )
title('NMR spectrum and optimal smooth')
xlabel('Channel')
ylabel('Signal strength')






