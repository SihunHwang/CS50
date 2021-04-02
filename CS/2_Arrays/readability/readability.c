#include <ctype.h>
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <math.h>

int calculate_cld(string text);

int main(void)
{
    string text = get_string("Text: ");
    int cld = calculate_cld(text);
    
    if (cld < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (cld >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", cld);
    }
    
}

int calculate_cld(string text)
{
    float sentences = 0.0; // num of .!?
    float words = 1.0; //num of spaces
    float letters = 0.0; //num of alphabet

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char c = text[i];

        if (isalpha(c))
        {
            letters += 1;
        }
        else if (c == ' ')
        {
            words += 1;
        }
        else if (c == '.' || c == '?' || c == '!')
        {
            sentences += 1;
        }
        else{
            continue;
        }
    }

    float L = 100 * (letters / words);
    float S = 100 * (sentences / words);
    float cld = 0.0588 * L - 0.296 * S - 15.8;
    
    return round(cld);
}