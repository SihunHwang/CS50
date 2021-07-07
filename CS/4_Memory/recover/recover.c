#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int is_jpeg(int a, int b, int c, int d);

int main(int argc, char *argv[])
{
    if (argc != 2){
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    int c = 0;
    char filename[10];
    uint8_t *buffer;
    FILE *output = NULL;

    buffer = (uint8_t*)malloc(512 * sizeof(uint8_t));

    while (fread(buffer, 512, 1, input)){

        if (is_jpeg(buffer[0], buffer[1], buffer[2], buffer[3])){

            if (c != 0){

                fclose(output);
            }

            sprintf(filename, "%03i.jpg",c);
            output = fopen(filename, "w");
            c++;

        }

        if (c != 0){

            fwrite(buffer, 512, 1, output);
        }
    }
    fclose(input);
    fclose(output);
    return 0;
}

int is_jpeg(int a, int b, int c, int d)
{
    if (a != 0xff){
        return 0;
    }

    if (b != 0xd8){
        return 0;
    }

    if (c != 0xff){
        return 0;
    }

    if ((d & 0xf0) != 0xe0){
        return 0;
    }

    return 1;
}