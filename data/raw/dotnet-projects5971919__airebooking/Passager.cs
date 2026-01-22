namespace AireBooking.Models
{
    public class Passager
    {
        public int Id { get; set; }
        public string Nom { get; set; }
        public string Prenom { get; set; }
        public string Tel { get; set; }
        public string Password { get; set; }

        public Voiture Voiture { get; set; } // 1..1

        public List<Reservation> Reservations { get; set; } = new(); // 0..*
    }
}
