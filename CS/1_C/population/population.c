#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int p;
    do
    {
        p = get_int("Start size: ");
    }
    while (p < 9);
    
    // TODO: Prompt for end size
    int e;
    do
    {
        e = get_int("End size: ");
    }
    while (e < p);
    
    // TODO: Calculate number of years until we reach threshold
    int year = 0;
    while (true)
    {
        if (p >= e)
        {
            break;
        }
        
        int born = p / 3;
        int dead = p / 4;
        
        p = p + born - dead;
        year += 1;
    }
    
    // TODO: Print number of years
    printf("Years: %i\n", year);
}