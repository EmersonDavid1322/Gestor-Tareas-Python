import discord
from discord.ext import commands
from datetime import datetime
import random
import os
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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"⚠️ Error: Te falta el argumento \nConsulta el comando `!ayuda` para mas información")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"⚠️ Error: Tipo de argumento incorrecto \nConsulta el comando `!ayuda` para mas información")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f"⚠️ Error: Comando no encontrado \nConsulta el comando `!ayuda` para mas información")
    else:
        raise error
    

@bot.command()
async def tareas_l (ctx):
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
    if not tareas_rutina:
        await ctx.send("No hay tareas pendientes. ¡Día libre! ☕")
        return

    mensaje = "**📋 TUS TAREAS ACTUALES:**\n"

    for i, tarea in enumerate(tareas_rutina, start=1):
        if not tarea.estado == "Pendiente":
            estado = "✅"
        if fecha_hoy in str(tarea.estado):
            estado = "✅"
        else:
            estado = "❌"
        racha_visual = "🔥" * tarea.racha
        if tarea.racha == 0:
            tarea.racha = "No hay racha"
        mensaje += f"\n{i}. {estado} **{tarea.nombre}** \nHora: {tarea.hora} \nDias: {tarea.dias} \n({tarea.racha} {racha_visual})"
    
    await ctx.send(mensaje)

@bot.command()
async def hecho(ctx, numero: int):
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
        historial.append(f"Habito de {tarea.nombre} completo \n racha de dias {tarea.racha}")

        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal) 
        await ctx.send(f"⭐ ¡Muy bien! Has completado: **{tarea.nombre}**")
        racha_visual = "🔥" * tarea.racha
        await ctx.send(f"Tu racha actual es: ({tarea.racha} {racha_visual})")
        
    except IndexError:
        await ctx.send("Ese número de tarea no existe \n Revisa la lista con `!tareas`.")

@bot.command()
async def fallo(ctx, numero: int):
    tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
    indice_real = numero -1
    try:
        tarea = tareas_rutina[indice_real]
        if indice_real < 0:
            raise IndexError
        
    
        await ctx.send(f"La racha de la tarea **{tarea.nombre}** se reinicio a 0 \n racha de **🔥{tarea.racha}** días perdida")
        tarea.racha = 0
        tarea.estado = "Pendiente"
        guardar_datos(tareas, historial, puntos,tareas_rutina,registro_cumplidos,webhook,lista_frases,usar_frase,token,canal) 

    except IndexError:
        await ctx.send("Ese número de tarea no existe \n Revisa la lista con `!tareas`.")
        

@bot.command()
async def estadisticas(ctx, tipo_lista: str):
    tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
    if tipo_lista== "tarea":
        lista = tareas
    elif tipo_lista == "rutina":
        lista = tareas_rutina
    else:
        await ctx.send(f"Opcion no valida, solo disponieble 'tarea' y 'rutina' \n Consulte el comando `!ayuda` para mas información")

    await ctx.send(f"La cantidad de tareas registradas son: {len(lista)}\n")

    completadas = sum(1 for t in lista if t.estado != "Pendiente\n")
    await ctx.send(f"La cantidad de tareas Completadas son: {completadas}")

    pendientes = sum(1 for t in lista if t.estado == "Pendiente")
    await ctx.send(f"La cantidad de tareas pendientes son: {pendientes}\n")
    if len(lista) == 0:
        porcentaje_c = 0
    else:
        porcentaje_c = (completadas / len(lista)) * 100

    if len(lista) == 0:
        porcentaje_p = 0
    else:
        porcentaje_p = (pendientes / len(lista)) * 100
    await ctx.send(f"El porcentaje de tareas completas es de: {porcentaje_c:.2f}%")
    await ctx.send(f"El porcentaje de tareas pendientes es de: {porcentaje_p:.2f}%\n")

    bloques = int(porcentaje_c / 10)
    barra = "🟦" * bloques + "⬜" * (10 - bloques)
    await ctx.send(f"Progreso: [{barra}] {porcentaje_c:.2f}%")

@bot.command()
async def racha(ctx):
    tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
    max_racha = max(t.racha for t in tareas_rutina)
    tarea_top = next(t for t in tareas_rutina if t.racha == max_racha)
    
    fuego = "🔥" * (max_racha if max_racha <= 10 else 10)
    await ctx.send(f"🏆 **Tu mayor racha actual es en:** {tarea_top.nombre}\n**Días:** {max_racha} {fuego}")

@bot.command()
async def frases(ctx):
    tareas, historial, puntos, tareas_rutina, registro_cumplidos,webhook, lista_frases, usar_frase, token, canal = cargar_datos()
    if len(lista_frases) == 0:
        await ctx.send("**La fotaleza del hombre radica en el dominio de su mente**")
    else:
        eleccion = random.choice(lista_frases)
        embed = discord.Embed(
        description=f"### *\"{eleccion}\"*",
        color=discord.Color.dark_gold()
        )
        embed.set_footer(text="Mantente en el camino. 🔥")
        await ctx.send(embed=embed)

@bot.command()
async def ayuda(ctx):
    embed = discord.Embed(
        title="Guía del Gestor de Tareas 📋",
        description="¿Deseas gestionar tus tareas? ejecuta el scrips 'main_menu' y tendras todas las opciones disponibles\n \nAquí tienes los comandos disponibles para mantener tu disciplina:",
        color=discord.Color.blue()
    )
    
    embed.add_field(name="`!tareas_l`", value="Lista todos tus hábitos y su estado actual.", inline=False)
    embed.add_field(name="`!hecho [número]`", value="Marca el hábito como completado hoy y sube tu racha. 🔥", inline=False)
    embed.add_field(name="`!fallo [número]`", value="Marca el hábito como fallido reiniciando la racha y su estado", inline=False)
    embed.add_field(name="`!estadisticas`", value="Muesta las estadisticas de tus tareas y rutinas, argumentos disponibles 'tarea' y 'rutina'.", inline=False)
    embed.add_field(name="`!racha`", value="Muesta tu mejor racha actualmente junto con la cantidad de días.", inline=False)
    embed.add_field(name="`!frases`", value="Muesta frases aletorias que hayas añadido en la lista de frases.", inline=False)
    embed.add_field(name="`!ayuda`", value="Muestra este mensaje de soporte.", inline=False)

    embed.set_footer(text="¡Sigue en el camino asi!")
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    bot.run(token)
