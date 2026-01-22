namespace AireBooking.Models
{
    public class Ville
    {
        public int Id { get; set; }
        public string Libelle { get; set; }

        public List<Aire> Aires { get; set; } = new();
    }
}
