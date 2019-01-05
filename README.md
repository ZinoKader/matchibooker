# matchibooker
Schedules bookings for Matchi.se (racket sports booking site)

A tool to circumvent same-day booking restrictions on Matchi.se.
When a tennis time-slot is bookable (only on the same day, earliest at 00:00), matchibooker will 
book it for you automatically as soon as possible. Set preferred time slots and matchibooker will try to book the prefered ones
in order if they're still available when the job is executed at 00:00.
