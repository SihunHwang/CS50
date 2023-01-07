// Implements a dictionary's functionality
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 100000;
int SIZE = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int hash_index = hash(word);

    node *cursor = table[hash_index];

    while (cursor != NULL)
    {
        if (strcasecmp(word, (*cursor).word) == 0)
        {
            return true;
        }

        cursor = (*cursor).next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    //djb2 by Dan Bernstein
    unsigned int hash = 5381;
    int c;

    while ((c = *word++))
    {
        c = tolower(c);

        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }

    if (hash >= N)
    {
        hash = hash % N;
    }

    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open
    FILE* file = fopen(dictionary,"r");
    if (file == NULL)
    {
        return false;
    }

    char buffer[LENGTH + 1];
    while (fscanf(file, "%s", buffer) != EOF)
    {
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        strcpy((*n).word, buffer);

        int hash_index = hash((*n).word);

        (*n).next = table[hash_index];

        table[hash_index] = n;

        SIZE++;
    }

    fclose(file);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return SIZE;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    node *cursor;
    node *tmp;


    for (int i = 0; i < N; i++)
    {
        cursor = table[i];

        while (cursor != NULL)
        {
            tmp = cursor;

            cursor = (*cursor).next;

            free(tmp);
        }
    }

    return true;
}
