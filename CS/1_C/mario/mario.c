#include <stdio.h>
#include <cs50.h>
#include <string.h>
void draw(int n, int h);

int main(void)
{
    //prompt user for height
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h < 1 || h > 8);
    
    //build the pyramid
    for (int i = 1; i <= h; i++)
    {
        draw(i, h);
    }
}


void draw(int n, int h)
{
    int spaces = h - n;
    
    for (int i = 0; i < spaces; i++)
    {
        printf(" ");
    }
    
    for (int i = 0; i < n; i++)
    {
        printf("#");
    }
    printf("  ");
    for (int i = 0; i < n; i++)
    {
        printf("#");
    }
    printf("\n");
}
