#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    //prompt user for card number
    long long int number = get_long("Number: ");

    //calculate checksum
    int checksum = 0;
    int d = 0;
    long long int i = 1;
    while (true)
    {
        i *= 10;
        d += 1;
        int x = floor((number % i) / (i / 10));
        
        if (d % 2 == 0)
        {
            x *= 2;
            if (x >= 10)
            {
                x = 1 + (x % 10);
            }
        }

        checksum += x;

        if ((long double) number / (long double) i < 1)
        {
            break;
        }
    }
    

    //classify the card
    if (checksum % 10 != 0)
    {
        printf("INVALID\n");
    }
    else
    {
        int f2d = floor((number % i) / (i / 100));

        if ((f2d == 34 || f2d == 37) && d == 15)
        {
            printf("AMEX\n");
        }
        else if (f2d >= 51 && f2d <= 55 && d == 16)
        {
            printf("MASTERCARD\n");
        }
        else if ((d == 13 || d == 16) && f2d <= 49 && f2d >= 40)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }

}