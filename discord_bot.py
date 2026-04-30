import discord
from discord.ext import commands
from datetime import datetime
from storage import guardar_datos, cargar_datos
tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()

intents = discord.Intents.all()
intents.message_content = True 

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
    print(f'✅ Bot conectado como {bot.user}')
    try:
        id_canal = int(canal)
        canal_eventos = bot.get_channel(id_canal)

        if canal_eventos:
            await canal_eventos.send("**Bot conectado y funcionando correctamente**\n")
        else:
                print(f"❌ No pude encontrar el canal con ID: {id_canal}. ¿El bot está en ese servidor?")
    except ValueError:
        print(f"❌ Error: El ID del canal guardado ('{canal}') no es un número válido.")

@bot.command(help="Muestra la lista de tus hábitos y tareas pendientes.")
async def tareas(ctx):
    tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
    if not tareas_rutina:
        await ctx.send("No hay tareas pendientes. ¡Día libre! ☕")
        return

    mensaje = "**📋 TUS TAREAS ACTUALES:**\n"

    for i, tarea in enumerate(tareas_rutina, start=1):
        estado = "✅" if not tarea.estado == "Pendiente"  else "❌"
        mensaje += f"{i}. {estado} **{tarea.nombre}** \nHora: {tarea.hora} \nDias: {tarea.dias} \n(🔥 {tarea.racha})\n"
    
    await ctx.send(mensaje)

@bot.command(help="Marca una tarea como completada usando su número. Ejemplo: !completar 1")
async def completar(ctx, numero: int):
    tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
    fecha = datetime.now()
    fecha_m = fecha.strftime("%d/%m/%Y")
    
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    indice_real = numero -1

    try:
        tarea = tareas_rutina[indice_real]
        if indice_real < 0:
            raise IndexError
        if fecha_hoy in str(tarea.estado):
            await ctx.send(f"⚠️ La tarea **{tarea.nombre}** ya ha sido marcada como completa hoy.")
            return

        tarea.estado = f"Habito completado el {fecha_m}"
        tarea.racha += 1
        registro_cumplidos.append({
                "Nombre": tarea.nombre,
                "Estado": tarea.estado,
                "Prioridad": tarea.prioridad,
                "Racha": tarea.racha
            })

        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal) 
        await ctx.send(f"⭐ ¡Muy bien! Has completado: **{tarea.nombre}**")
        
    except IndexError:
        await ctx.send("Ese número de tarea no existe \n Revisa la lista con `!tareas`.")

@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(
        title="Guía del Gestor de Tareas 📋",
        description="Aquí tienes los comandos disponibles para mantener tu disciplina:",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="`!tareas`", value="Lista todos tus hábitos y su estado actual.", inline=False)
    embed.add_field(name="`!hecho [número]`", value="Marca el hábito como completado hoy y sube tu racha. 🔥", inline=False)
    embed.add_field(name="`!ayuda`", value="Muestra este mensaje de soporte.", inline=False)
    
    embed.set_footer(text="¡Sigue en el camino asi!")
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(token)
