#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int main(int argc, string argv[])
{
    //check if key is valid
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    
    int length = strlen(argv[1]);
    
    if (length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    
    char upper[length];
    
    for (int i = 0; i < length; i++)
    {
        if (isalpha(argv[1][i]))
        {
            //change key to uppercase
            upper[i] = toupper(argv[1][i]);
        
            //check for duplicates
            for (int j = 0; j < i; j++)
            {
                if (i == 0){continue;}
                if (upper[i] == upper[j])
                {
                    printf("Key must contain 26 characters.\n");
                    return 1;
                }
            }
        }
        else
        {
            printf("Key must contain 26 characters.\n");
            return 1;
        }
    }
    
    
    string plaintext = get_string("plaintext: ");
    int len = strlen(plaintext);
    
    printf("ciphertext: ");
    
    for (int i = 0; i < len; i++)
    {
        char c = plaintext[i];
        
        if (isalpha(c))
        {
            if (isupper(c))
            {
                c = upper[c - 65];
            }
            else
            {
                c = upper[c - 97] + 32;
            }
        }
        printf("%c", c);
    }
    printf("\n");
    return 0;
    
}

