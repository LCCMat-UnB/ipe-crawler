namespace AireBooking.Models
{
    public class Aire
    {
        public int Id { get; set; }
        public string Nom { get; set; }
        public int Capacite { get; set; }

        public int VilleId { get; set; } // 1..1
        public Ville Ville { get; set; }

        public List<Reservation> Reservations { get; set; } = new(); // 1..*
    }
}
