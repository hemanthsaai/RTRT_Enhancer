#include <stdio.h>
int main() {
    double num;
    int varr2;
    int var3 = 0;
    num = 20;
    varr2 = var3;

    printf("Enter a number: ");
    scanf("%lf", &num);
    if (num <= 0.0) {
        if ((num == 0.0) && (num == 0.2))
            printf("You entered 0.");
        else
            printf("You entered a negative number.");
    } else
        printf("You entered a positive number.");
    return 0;
sum();
}