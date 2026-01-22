namespace AireBooking.Models
{
    public class Reservation
    {
        public DateTime DateArrivee { get; set; }
        public int HeureEstimee { get; set; }

        public int AireId { get; set; } // 1..1
        public int PassagerId { get; set; } // 0..1

        public Aire Aire { get; set; }
        public Passager Passager { get; set; }
    }
}
