clear all;
close all;
%read the grayscale input lena image 
x=imread("camera.tif");
% x = imread("headCT.tif");

% x = imread("mandril_gray.tif");
% x = imread("pirate.tif");
%x = x/ max(x(:));

imshow(x);

%initally remove the noise by smoothening or blurring the gray scale image
%using a Gaussian Kerenl 

[row, columns] = size(x);

%create the gaussian kernel
% m - size of gaussain kernel 
m = 5; 
K= 1;

% sigma 
sigma = 3; 
%create a matrix g for gausian kernel of size m*m

g = zeros(m,m);
for i= 1:1:m
 for j = 1:1:m
 %compute the exponential part of the formula given in textbook eq 3-45
 exp_numpart = -[((i-((m-1)/2)-1).^2) ];
 exp_denpart = 2*sigma *sigma;
 g(i , j) = K*exp(exp_numpart/ exp_denpart);
 end
end

%normalize the weights 
g_norm = g / sum (g(:));

%performs convolution of the image with the 
g_norm_transpose = transpose(g_norm);

conv_output_horizontal = conv2(x, g_norm, 'same');

conv_output_vertical = conv2(conv_output_horizontal, g_norm_transpose, 'same');

figure;

imshow(uint8(conv_output_horizontal));
title("blurred image");


figure;

imshow(uint8(conv_output_vertical));
title('image blurred vertical');
%once we perform Gaussain smoothening to remove the noise , next we need to
%get the edge detection using derivatives using horizontal and vertical
%direction 

%this is done using the sobel filter

Sobel_horizontal = [-1 0 1 ; -2 0 2; -1 0 1];

Sobel_vertical = [ 1 2 1;0 0 0;-1 -2 -1];


%extracting edge by using horizontal filter

sobel_conv_h = conv2(conv_output_vertical, Sobel_horizontal, 'same');

figure;

imshow(uint8(sobel_conv_h));
title('sobel hosrizontal detection ');

%extracting edge by using vertical filter

sobel_conv_v = conv2(conv_output_vertical, Sobel_vertical, 'same');

figure;

imshow(uint8(sobel_conv_v));
title('vertical detection ');


%computes the gradient of the horizontal and vertical edge detected image
%using sqrt function 

magnitude = sqrt(sobel_conv_v.^2 + sobel_conv_h.^2);

normalized = magnitude / max(magnitude(:));

figure;
imshow((normalized));
title('magnitude'); 

%calculate the angle theta - which denotes the slope of the gradient 


theta = atan2(sobel_conv_h, sobel_conv_v ) * 180 /pi;

figure;
imshow(uint8(theta));
title('angle');

%converts the negative angle to posititve for further processing and
%simplicity 
for i = 1:row
    for j = 1:columns
        if (theta(i,j) < 0 )
            theta(i,j) = theta(i,j) + 180;
        end
    end
end
% theta = theta;
% normalized = normalized;
% 
%%%%%%implenentation of maximal suppression to get rid of the thick edges
%%%%%%using the angle of the gradient image from edge detection 

%in order to get better performance for canny we use interpolation for the angle
%and gradient magnitude to get better estimation
[row, columns] = size(normalized);
[X, Y] = meshgrid(1:row, 1:columns);
[Xq, Yq] = meshgrid(1:0.5:row, 1:0.5:columns);

magnitude_interp = interp2(X, Y, normalized, Xq, Yq, "cubic");
direction_interp = interp2(X, Y, theta, Xq, Yq, "cubic");



[newrow, newcolumns] = size(magnitude_interp);



supress_arr = zeros(newrow, newcolumns);
% i =2;
% j=2;

for i = 2:newrow -1
   for j = 2:newcolumns-1
        curr_pixel = magnitude_interp(i,j);
   
         %%for given i,j get 3*3 neighbour values ,convert to 1d get the
         %%interpolated and use tht for magnitude
          %%grad_interp (1,9 ) is normalized(i,j)
%         row_grad = [  normalized(i-1,j-1), normalized(i-1,j), normalized(i-1,j+1),  normalized(i, j-1),  normalized(i,j),  normalized(i, j+1),normalized(i+1, j-1),  normalized(i+1,j),  normalized(i+1, j+1)];
        
%         x1 = 1:0.5:9;
          
%         grad_interpx = interp1( row_grad, x1, 'pchip');

       %%interpolation of the angle theta 

%        row_theta =  [  theta(i-1,j-1), theta(i-1,j), theta(i-1,j+1),  theta(i, j-1),  theta(i,j),  theta(i, j+1), theta(i+1, j-1),  theta(i+1,j),  theta(i+1, j+1)];
%         x2 = 1:0.5:9;
       
%        angle_interp = interp1(row_theta, x2, 'pchip');
         
%        theta(i,j) = (angle_interp(1,8) + angle_interp(1,10)) / 2;
 
        if (direction_interp(i,j) < 22.5 && direction_interp(i,j) >= 0  ) || ( direction_interp(i,j) <= 180 && direction_interp(i,j) >= 157.5 )

         ang = 0;   %%here we consider only horizontal neighbours
        elseif ( direction_interp(i,j) >=22.5 &&  direction_interp(i,j) < 67.5 )
            ang = -45; %%here we consider diagonal righ to left as neighbours for comparison 

        elseif (  direction_interp(i,j) < 112.5 && direction_interp(i,j) >=67.5 )
            ang = 90; %% here angle is considered to be at 90 degrees 

        elseif (direction_interp(i,j) >= 112.5 && direction_interp(i,j) < 157.5)
            ang = 45; %%diagonal from right to left considered

        end

       if(ang == 0  && (magnitude_interp(i+1, j) <= curr_pixel && magnitude_interp(i-1, j) <= curr_pixel))

          supress_arr(i,j) = magnitude_interp(i,j);

       elseif (ang == -45 && (magnitude_interp(i-1, j+1) <= curr_pixel && magnitude_interp(i+1, j-1) <= curr_pixel))
%          elseif (ang == -45 && (grad_interpx(1,4) <= curr_pixel && grad_interpx(1,13) <= curr_pixel))
             supress_arr(i,j) = magnitude_interp(i,j); 

           elseif(ang == 90  && (magnitude_interp(i, j-1) <= curr_pixel && magnitude_interp(i, j+1) <= curr_pixel))
%        elseif (ang == 90  && (grad_interpx(1,8) <= curr_pixel && grad_interpx(1,10) <= curr_pixel))

            supress_arr(i,j) = magnitude_interp(i,j);

           elseif(ang == 45 && (magnitude_interp(i-1, j-1) <= curr_pixel && magnitude_interp(i+1, j+1) <= curr_pixel))
%        elseif (ang == 45 && (grad_interpx(1,2) <= curr_pixel && grad_interpx(1,16) <= curr_pixel))
            supress_arr(i,j) = magnitude_interp(i,j); 
       
           else 
             supress_arr(i,j) = 0;

       end
 


%         j = j+1;
        
        
    end
%     i = i+1;
end

supress_arr = downsample(downsample(supress_arr,2)',2)';

supress_arr = 1*supress_arr/ max(supress_arr(:));

figure;
imshow((supress_arr));
title(" non maximal suppression");



%%%%%%%next we perform hysteris thresholding or double thresholding
%%%%%%%procedure to remvoe the edge points that are not true 
%select threshold parameters

high_thresh = 1.0;    
% * max(max(supress_arr));

low_thresh = 0.15;    
% high_thresh;


gnh = zeros(row, columns);  
gnl = zeros(row, columns);

for i = 1:row
    for j =1:columns
      if(supress_arr(i,j) >= low_thresh)
        gnl(i,j) = 1;
      end
      if (supress_arr(i,j) >= high_thresh)
          gnh(i,j) = 1;
      end

    end
end


gnl = gnl - gnh;
%retain 
figure;
imshow((gnl));
title("low threshold");


figure;
imshow((gnh));
title("high threshold");


%%%%implementation of connectivity 

%here we use 8 connectivity to check if any image pixel intensity is
%surrounded by a strong threshold pixel 
%%here the non zero pixel intensity in high threshold image gnh is taken as
%%'strong' pixel and the non zero pixel in low threshold image is weak
%%pixel 

gnl_connect =gnl;
visited = zeros(row, columns);
%modifed of gnl 
for i =2:row-1
    for j = 2:columns-1
        
    if( gnh(i,j)== 1)
         visited(i,j)=1;
%         if(gnl(i-1,j-1)==1 && gnl(i-1, j)==1 && gnl(i-1, j+1) ==1 && gnl(i, j-1) == 1 && gnl(i, j+1) ==1 && gnl(i+1, j-1)==1 &&  gnl(i+1, j)==1 && gnl(i+1, j+1)==1  )
          gnl_connect(i-1,j-1)= 1; gnl_connect(i-1, j) = 1; gnl_connect(i-1, j+1) =1;
          gnl_connect(i, j-1) = 1; gnl_connect(i, j+1) =1; gnl_connect(i+1, j-1) =1;
          gnl_connect(i+1, j) =1; gnl_connect(i+1, j+1) =1;
          gnl_connect(i,j)=1;
    end
    
   end
end

gn_new = zeros(row, columns);
for i =2:row-1
    for j = 2:columns-1
%        if(visited(i,j)==0)
%            gnl(i,j)=0; // element wise gnl with subtraction 
        gnl_connect(i,j)= gnl(i,j) * gnl_connect(i,j); 
%        gnh(i,j) = gnh(i,j) | gn_new(i,j);
    end
end

%%%append to gnh all the valid pixels from modified gnl above 


final_img = gnh | gnl_connect;

% final_img = final_img/ max(max(final_img(:)));


figure;
imshow((final_img));
title("final image")

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%comparison with the inbuit canny output 
canny_input = imread("lena_gray_512.tif");


% canny_input = imread("headCT.tif");
% canny_input = imread("mandril_gray.tif");

%x = imread("mandril_gray.tif");
%defining the input parameters for the inbuit function 
sigma = 3;     
lower_threshold = 0.15; 
upper_threshold = 1.0; 

thresh = lower_threshold*upper_threshold;

canny_out = edge(canny_input, 'Canny', thresh, sigma);


figure;
imshow(canny_out);
title('Canny Inbuit function matlab output'); 


% diff = abs(final_img- canny_out ).^2;Mean_square_error = sum(diff(:))/numel(final_img);
% MSE = (Mean_square_error);

MSE = immse(double(final_img), double(canny_out));






