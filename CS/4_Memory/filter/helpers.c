#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++){

        for (int j = 0; j < width; j++){

            float c = (image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3.0;
            c = round(c);

            RGBTRIPLE rgb;
            rgb.rgbtBlue = c;
            rgb.rgbtRed = c;
            rgb.rgbtGreen = c;

            image[i][j] = rgb;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE memory;

    for (int i = 0; i < height; i++){

        for (int j = 0; j < width/2; j++){

            memory = image[i][j];

            image[i][j] = image[i][width - 1 - j];

            image[i][width - 1 - j] = memory;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++){

        for (int j = 0; j < width; j++){

            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++){

        for (int j = 0; j < width; j++){

            float r = 0;
            float g = 0;
            float b = 0;
            float n = 0;

            if (i - 1 >= 0){

                if (j - 1 >= 0){

                    r += copy[i - 1][j - 1].rgbtRed;
                    g += copy[i - 1][j - 1].rgbtGreen;
                    b += copy[i - 1][j - 1].rgbtBlue;
                    n += 1;
                }

                r += copy[i - 1][j].rgbtRed;
                g += copy[i - 1][j].rgbtGreen;
                b += copy[i - 1][j].rgbtBlue;
                n += 1;

                if (j + 1 < width){

                    r += copy[i - 1][j + 1].rgbtRed;
                    g += copy[i - 1][j + 1].rgbtGreen;
                    b += copy[i - 1][j + 1].rgbtBlue;
                    n += 1;
                }
            }


            if (j - 1 >= 0){

                r += copy[i][j - 1].rgbtRed;
                g += copy[i][j - 1].rgbtGreen;
                b += copy[i][j - 1].rgbtBlue;
                n += 1;
            }

            r += copy[i][j].rgbtRed;
            g += copy[i][j].rgbtGreen;
            b += copy[i][j].rgbtBlue;
            n += 1;

            if (j + 1 < width){

                r += copy[i][j + 1].rgbtRed;
                g += copy[i][j + 1].rgbtGreen;
                b += copy[i][j + 1].rgbtBlue;
                n += 1;
            }

            if (i + 1 < height){

                if (j - 1 >= 0){

                    r += copy[i + 1][j - 1].rgbtRed;
                    g += copy[i + 1][j - 1].rgbtGreen;
                    b += copy[i + 1][j - 1].rgbtBlue;
                    n += 1;
                }

                r += copy[i + 1][j].rgbtRed;
                g += copy[i + 1][j].rgbtGreen;
                b += copy[i + 1][j].rgbtBlue;
                n += 1;

                if (j + 1 < width){

                    r += copy[i + 1][j + 1].rgbtRed;
                    g += copy[i + 1][j + 1].rgbtGreen;
                    b += copy[i + 1][j + 1].rgbtBlue;
                    n += 1;
                }
            }

            RGBTRIPLE rgb;
            rgb.rgbtRed = round(r / n);
            rgb.rgbtGreen = round(g / n);
            rgb.rgbtBlue = round(b / n);

            image[i][j] = rgb;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++){

        for (int j = 0; j < width; j++){

            copy[i][j] = image[i][j];
        }
    }

    int x[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int y[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    for (int i = 0; i < height; i++){

        for (int j = 0; j < width; j++){

            float rx = 0;
            float ry = 0;
            float gx = 0;
            float gy = 0;
            float bx = 0;
            float by = 0;

            for (int k = -1; k < 2; k++){

                if ((i + k < 0) || (i + k >= height)){

                    continue;
                }

                for (int l = -1; l < 2; l++){

                    if ((j + l < 0) || (j + l >= width)){

                        continue;
                    }

                    rx += copy[i + k][j + l].rgbtRed * x[k + 1][l + 1];
                    gx += copy[i + k][j + l].rgbtGreen * x[k + 1][l + 1];
                    bx += copy[i + k][j + l].rgbtBlue * x[k + 1][l + 1];

                    ry += copy[i + k][j + l].rgbtRed * y[k + 1][l + 1];
                    gy += copy[i + k][j + l].rgbtGreen * y[k + 1][l + 1];
                    by += copy[i + k][j + l].rgbtBlue * y[k + 1][l + 1];
                }
            }

            int r = round(sqrt(rx * rx + ry * ry));
            int g = round(sqrt(gx * gx + gy * gy));
            int b = round(sqrt(bx * bx + by * by));

            if (r > 255){
                r = 255;
            }
            if (g > 255){
                g = 255;
            }
            if (b > 255){
                b = 255;
            }

            image[i][j].rgbtRed = r;
            image[i][j].rgbtGreen = g;
            image[i][j].rgbtBlue = b;
        }
    }

    return;
}
