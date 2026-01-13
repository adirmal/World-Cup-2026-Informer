package bgu.spl.net.srv;
import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;

public class ConnectionsIMPL<T> implements Connections<T> {
    private Map<Integer, ConnectionHandler<T>> ch_map = new ConcurrentHashMap<>();
    private Map<String, Map<Integer, String>> channelSubscribers = new ConcurrentHashMap<>();

    @Override
    public boolean send(int connectionId, T msg) {
        ConnectionHandler<T> curr_Handler = ch_map.get(connectionId);
        if (curr_Handler != null) {
            curr_Handler.send(msg);
            return true;
        }
        return false;
    }

    @Override
    public void send(String channel, T msg) {
        Map<Integer, String> subs = channelSubscribers.get(channel);
        if (subs != null) {
            for (Map.Entry<Integer, String> entry : subs.entrySet()) {
                Integer ch_id = entry.getKey();
                send(ch_id,msg);
            }
        }
    }
        
    @Override
    public void disconnect(int connectionId) {
        ch_map.remove(connectionId);
        for (Map<Integer, String> subs : channelSubscribers.values()) {
                subs.remove(connectionId);
            }
    }

    public void connect(int connectionId, ConnectionHandler<T> ch) {
        ch_map.put(connectionId, ch);
    }

    public void subscribe(int connectionId, String channelString, String subscriptionId) {
        Map<Integer, String> channel = channelSubscribers.get(channelString);
        if (channel == null) {
            channel = new ConcurrentHashMap<>();
            Map<Integer, String> existingChannel = channelSubscribers.putIfAbsent(channelString, channel);
            if (existingChannel != null)  {
                channel = existingChannel;
            }
        }
        channel.put(connectionId, subscriptionId);
    }

    public void unsubscribe(int connectionId, String channelString) {
        Map<Integer, String> channel = channelSubscribers.get(channelString);
        if (channel != null) {
            channel.remove(connectionId);
        }
    }
}
