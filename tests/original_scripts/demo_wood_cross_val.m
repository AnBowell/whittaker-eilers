% Demonstration wood smoothing with Whittaker smoother
% Optimal smoothing by cross-validation
%
% Paul Eilers, 2003

% Get the data
y = load('wood.txt');


weights_one = zeros(1, length(y));
for i = 1:1:length(y)
    if mod(i, 10) == 0
        weights_one(i) = 1;
    end
end

x_input =  1:1:length(y);

disp(y)

% Smooth for series of lambdas
lambdas = 10 .^ (-2:0.2:8);
cvs = [];
for lambda = lambdas
   %[z cv] = whitsmw(y, weights_one', lambda, 2);
   [z cv] = whitsmdd(transpose(x_input(1:5:length(y))), y(1:5:length(y)), lambda, 2);
   %[z cv] = whitsmddw(transpose(x_input), y,transpose(weights_one), lambda, 2);
   cvs = [cvs cv];
end


% Choose optimal lambda
[cm ci] = min(cvs);
lambda = lambdas(ci);
[z cv] = whitsm(y, lambda, 2);

% Plot data and smooth
subplot(2, 1, 1);
plot([y z] )    % Downward shift for visibility
title('Wood optmial smooth')
xlabel('Channel')
ylabel('Signal strength')

% Plot CV profile
subplot(2, 1, 2)
semilogx(lambdas, cvs)
title('Cross-validation error')
xlabel('\lambda')
set(gcf, 'PaperPosition', [1 2 6 6])
ylim([5 7])
ylabel('CVE')



