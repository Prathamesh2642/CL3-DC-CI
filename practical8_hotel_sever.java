//to run this file - rename the file as HotelServer and other files as HotelInterface and HotelClient and ensure they are in same folder
//run HotelServer using - java HotelServer.java
//run HotelClient using - java HotelClient.java
import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.HashMap;
import java.util.Map;

public class HotelServer extends UnicastRemoteObject implements HotelServiceInterface {

    private Map<Integer, String> bookedRooms;

    public HotelServer() throws RemoteException {
        bookedRooms = new HashMap<>();
    }

    @Override
    public synchronized boolean bookRoom(String guestName, int roomNumber) throws RemoteException {
        if (!bookedRooms.containsKey(roomNumber)) {
            bookedRooms.put(roomNumber, guestName);
            System.out.println("Room " + roomNumber + " booked for guest: " + guestName);
            return true;
        } else {
            System.out.println("Room " + roomNumber + " is already booked.");
            return false;
        }
    }

    @Override
    public synchronized boolean cancelBooking(String guestName) throws RemoteException {
        for (Map.Entry<Integer, String> entry : bookedRooms.entrySet()) {
            if (entry.getValue().equals(guestName)) {
                bookedRooms.remove(entry.getKey());
                System.out.println("Booking for guest " + guestName + " canceled.");
                return true;
            }
        }
        return false; // No need to print an error message here
    }

    public static void main(String[] args) {
        try {
            HotelServer server = new HotelServer();
            // Create and export the RMI registry on port 1099
            java.rmi.registry.LocateRegistry.createRegistry(1099);
            // Bind the server object to the registry
            Naming.rebind("HotelService", server);
            System.out.println("Hotel Server is running...");
        } catch (RemoteException e) {
            e.printStackTrace();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
