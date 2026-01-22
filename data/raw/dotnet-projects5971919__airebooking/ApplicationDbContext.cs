using Microsoft.EntityFrameworkCore;
using AireBooking.Models;
using System.Collections.Generic;
using System.Reflection.Emit;

namespace AireBooking.Data
{
    public class ApplicationDbContext : DbContext
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<Aire> Aires { get; set; }
        public DbSet<Passager> Passagers { get; set; }
        public DbSet<Ville> Villes { get; set; }
        public DbSet<Reservation> Reservations { get; set; }
        public DbSet<Voiture> Voitures { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            modelBuilder.Entity<Aire>()
                .HasOne(a => a.Ville)
                .WithMany(v => v.Aires)
                .HasForeignKey(a => a.VilleId)
                .IsRequired();

            // Aire Passager via Reservation
            modelBuilder.Entity<Reservation>()
                .HasKey(r => new { r.AireId, r.PassagerId, r.DateArrivee });

            modelBuilder.Entity<Reservation>()
                .HasOne(r => r.Aire)
                .WithMany(a => a.Reservations)
                .HasForeignKey(r => r.AireId)
                .IsRequired();

            modelBuilder.Entity<Reservation>()
                .HasOne(r => r.Passager)
                .WithMany(p => p.Reservations)
                .HasForeignKey(r => r.PassagerId)
                .IsRequired(); 

            // Passager  Voiture
            modelBuilder.Entity<Passager>()
                .HasOne(p => p.Voiture)
                .WithOne(v => v.Passager)
                .HasForeignKey<Voiture>(v => v.PassagerId)
                .IsRequired(); 
        }
    }
}
