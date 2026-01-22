namespace AireBooking.Models
{
    public class Voiture
    {
        public int Id { get; set; }
        public string Matricule { get; set; }
        public string Type { get; set; }

        public int? PassagerId { get; set; } // 0..1
        public Passager? Passager { get; set; } 
    }
}
