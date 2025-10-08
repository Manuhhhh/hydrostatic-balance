class ArquimedesCalculator:
    def __init__(self, g_val=9.8, water_density=1000):
        self.g_val = g_val
        self.water_density = water_density

    def calculate_density(self, Wa, Ws):
        """
        Calcula la densidad del objeto usando el método de Arquímedes.
        Wa: peso en aire (N)
        Ws: peso sumergido en agua (N)
        """
        
        if Wa <= Ws:
            raise ValueError("Wa debe ser mayor que Ws (peso en aire > peso sumergido).")

        return (Wa / (Wa - Ws)) * self.water_density

    def calculate_mass(self, Wa):
        """Devuelve la masa del objeto (kg)."""
        return Wa / self.g_val

    def calculate_volume(self, Wa, Ws):
        """Devuelve el volumen del objeto (m³)."""
        return (Wa - Ws) / (self.water_density * self.g_val)

    def calculate_buoyant_force(self, Wa, Ws):
        """Devuelve el empuje (N)."""
        if Wa <= Ws:
            raise ValueError("Wa debe ser mayor que Ws (peso en aire > peso sumergido).")
        return Wa - Ws