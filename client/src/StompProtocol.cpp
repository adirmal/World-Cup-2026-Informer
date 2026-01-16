#include "../include/StompProtocol.h"
#include <iostream>
#include <stdlib.h>
#include <sstream>

StompProtocol::StompProtocol() : isConnected(false), subscriptionIdCounter(0), receiptIdCounter(0), 
                    currentUserName(""), gameToSubId(), subIdToGame() 
    {

    }
    
    std::string StompProtocol::processUserInput(std::string line) {
        
    }
    

