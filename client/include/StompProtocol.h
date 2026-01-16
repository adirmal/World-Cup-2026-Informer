#pragma once

#include "../include/ConnectionHandler.h"
#include <string>
#include <vector>
#include <map>

// TODO: implement the STOMP protocol
class StompProtocol
{
    private: 
        bool isConnected; 
        int subscriptionIdCounter;
        int receiptIdCounter;
        std::string currentUserName;

        //game to sub maps <->
        std::map<std::string, int> gameToSubId;
        std::map<int, std::string> subIdToGame;

    public:
        StompProtocol();
        std::string processUserInput(std::string line);
        bool processServerResponse(std::string frame);
        bool shouldTerminate();
        bool getIsConnected();
};
