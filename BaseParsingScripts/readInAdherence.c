#define MAXLEN 	1000

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct FileLine {
	char serviceDate[9];		// IGNORE
	int routes;					
	char block[7];				// IGNORE
	char routeDirect[12];		// IGNORE
	char stopNum[5];
	char location[47];			// IGNORE
	double latitude;		
	double longitude;
	int schedTime;				// IGNORE
	char schedTimeStr[8];		// IGNORE
	int arrTime;
	char arrTimeStr[8];			// IGNORE
	int depTime;
	char depTimeStr[8];			// IGNORE
	float odometer;
	int vehicleNumber;			// IGNORE
} FileLine;

typedef struct NodeV {
	char stopNum[5];
	double longitude;
	double latitude;
	int index;
	struct NodeV * pNext;
} NodeV;

/*NodeV * insertLL(NodeV **ppHead, char stopNum[5]) {
	NodeV *pNew;
	NodeV *pFind;

	pNew = (NodeV *) malloc(sizeof(NodeV));
	strcpy(pNew->stopNum, stopNum);
	pNew->pNext = NULL;

	if (*ppHead == NULL) {
		*ppHead = pNew;
	} else {
		NodeV *current = *ppHead;
		for ( ; current != NULL; current = current->pNext) {
			if (current->pNext == NULL) {
				current->pNext = pNew;
				break;
			}
		}
	}
	return pNew;
}*/

void assignIndicies(NodeV * pRoot, int ind) {
	pRoot->index = ind;
	if (pRoot->pNext != NULL) {
		assignIndicies(pRoot->pNext, ind + 1);
	}
}

NodeV * searchEndV(NodeV *pRoot) {
	if (pRoot->pNext == NULL) {
		return pRoot;
	} else {
		return searchEndV(pRoot->pNext);
	}
}

NodeV * searchV(NodeV *pRoot, char stopNum[5]) {
	if (pRoot == NULL) {
		return NULL;
	} else if (strcmp(stopNum, pRoot->stopNum) == 0) {
		return pRoot;
	} else {
		return searchV(pRoot->pNext, stopNum);
	}
}

NodeV * allocateNodeV(char stopNum[5], double longitude, double latitude) {
	NodeV * pNew = malloc(sizeof(NodeV));
	strcpy(pNew->stopNum, stopNum);
	pNew->longitude = longitude;
	pNew->latitude = latitude;
	pNew->pNext = NULL;
	return pNew;
}

NodeV * insertV(NodeV * pRoot, char stopNum[5], double longitude, double latitude) {
	if (pRoot == NULL) {
		return allocateNodeV(stopNum, longitude, latitude);
	} else if (strcmp(stopNum, pRoot->stopNum) == 0) {
		return pRoot;
	} else {
		pRoot->pNext = insertV(pRoot->pNext, stopNum, longitude, latitude);
	}
	return pRoot;
}

int main(int argc, char * argv[]) {
	
	// ALLOWS THE USER TO PASS IN FILE NAME IN COMMAND
	int charcount = sizeof argv[1];
	char fileName[charcount];
	strcpy(fileName, argv[1]);

	// DECLARATION OF FILE
	FILE *pFileAdherence;

	// NECESSARY VALUES FOR THE READ IN
	char buffer[MAXLEN];
	char *file_line;
	int iScanfCnt;
	FileLine fl;
	FileLine pl;


	pFileAdherence = fopen(fileName, "r");
	fgets(buffer, MAXLEN, pFileAdherence);
	NodeV * pRoot = NULL;
	NodeV * pEnd = allocateNodeV("ERROR", 0.0, 0.0);
	int count = 0;

	while ((file_line = fgets(buffer, MAXLEN, pFileAdherence)) != NULL) {
		iScanfCnt = sscanf(file_line,"%*9[^,],%d,%*7[^,],%*12[^,],%5[^,],%*47[^,],%lf,%lf,%*d,%*8[^,],%d,%*8[^,],%d,%*8[^,],%f,%*d\n",
								&fl.routes,
								fl.stopNum,
								&fl.latitude,
								&fl.longitude,
								&fl.arrTime,
								&fl.depTime,
								&fl.odometer
							);

		pRoot = insertV(pRoot, fl.stopNum, fl.latitude, fl.longitude);

	}

	assignIndicies(pRoot, 0);
	pEnd = searchEndV(pRoot);
	printf("%d\n", pEnd->index);
	fclose(pFileAdherence);
}