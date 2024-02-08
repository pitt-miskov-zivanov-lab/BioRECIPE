#include "builder.h"


// Function to print out the diagram
void write_dd (DdManager *gbm, DdNode *dd, char* filename)
{
    FILE *outfile; // output file pointer for .dot file
    outfile = fopen(filename,"w");
    DdNode **ddnodearray = (DdNode**)malloc(sizeof(DdNode*)); // initialize the function array
    ddnodearray[0] = dd;
    Cudd_DumpDot(gbm, 1, ddnodearray, NULL, NULL, outfile); // dump the function to .dot file
    free(ddnodearray);
    fclose (outfile); // close the file */
}

// get a token from an entire line of text
const char* getfield(char* line, int num)
{
    const char* tok;
    for (tok = strtok(line, "|");
            tok && *tok;
            tok = strtok(NULL, "|\n"))
    {
        printf("token number %d is %s\n",num,tok);
        if (!--num)
            return tok;
    }
    return NULL;
}

void main_build(int species){


    // specifying how many reactants/products, and reaction rates
    int num_species = species;
    int num_reactions = 2;
    int num_reactants[] = {2,1};
    double k[] = {10,1};

    // creating diagram manager and nodes
    DdManager *manager;
    DdNode *total = NULL, *new_reaction, *temp, *var;
    manager = Cudd_Init(0,0,CUDD_UNIQUE_SLOTS,CUDD_CACHE_SLOTS,0); 

    for(int n=0; n<num_reactions; n++){
        // builds each reaction
        var = Cudd_addNewVar(manager);
        new_reaction = Cudd_addIte(manager, var, Cudd_addConst(manager, (CUDD_VALUE_TYPE)k[n]), Cudd_addConst(manager, (CUDD_VALUE_TYPE)0));
        for (int i=1; i<num_reactants[n]; i++){
            var = Cudd_addNewVar(manager);
            temp = Cudd_addIte(manager,var, new_reaction, Cudd_addConst(manager, (CUDD_VALUE_TYPE)0));
            Cudd_Ref(temp);
            Cudd_RecursiveDeref(manager, new_reaction);
            new_reaction = temp;
        }
        // adds reaction to the overall product delta function
        if(total != NULL){
            total = Cudd_addApply(manager, Cudd_addPlus, new_reaction, total);
        }
        else {
            total = new_reaction;
        }
    }

    // Output file information
    char filename1[30] = "out";
    FILE *out = fopen("BDD_Info.txt", "w");

    Cudd_PrintInfo(manager, out);
    fclose(out);
    write_dd(manager, total, filename1);
    Cudd_Quit(manager);
}


// when run by itself
int main (int argc, char *argv[])
{
    assert(argc == 2);
    printf("Starting CUDD\n");
    printf("%s\n", argv[1]);
    int species = atoi(argv[1]);

    main_build(species);

    return 0;
}
