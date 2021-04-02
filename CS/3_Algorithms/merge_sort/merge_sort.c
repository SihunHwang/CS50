#include <stdio.h>

#define MAX 24
int pairs[] = {4,6,8,3,2,43,4,6,24,2,5,5,53,6,5,7,97,0,46,24,64,75,35,4};

void merge_sort(int l, int r);
void merge(int l, int m, int r);



int main(void)
{
    merge_sort(0,MAX);
    
}

void merge_sort(int l, int r)
{
    if (l >= r)
    {
        return;
    }
    
    int m = (l + r) / 2;
    
    merge_sort(l, m);
    merge_sort(m + 1, r);
    
    merge(l, m, r);
    for (int i = 0; i < MAX; i++)
    {
        printf("%i ",pairs[i]);
    }
    printf("\n");
}

void merge(int l, int m, int r)
{
    int lenl = m - l + 1;
    int lenr = r - m;
    
    int left[lenl];
    int right[lenr];
    
    for (int i = 0; i < lenl; i++)
    {
        left[i] = pairs[i + l];
    }
    for (int j = 0; j < lenr; j++)
    {
        right[j] = pairs[j + m + 1];
    }
    
    int i = 0;
    int j = 0;
    int k = l;
    while (i < lenl && j < lenr)
    {
        if (left[i] > right[j])
        {
            pairs[k] = left[i];
            i += 1;
        }
        else
        {
            pairs[k] = right[j];
            j += 1;
        }
        k += 1;
    }
    while (i < lenl)
    {
        pairs[k] = left[i];
        k += 1;
        i += 1;
    }
    while (j < lenr)
    {
        pairs[k] = right[j];
        k += 1;
        j += 1;
    }
    
}