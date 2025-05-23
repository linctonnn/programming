import { REST, Routes }  from 'discord.js'

const commands = [
    {
        name: 'ping',
        description: 'Pong!',
    },
];

const rest = new REST({ version: '1'  }).setToken(TOKEN);

try {
    console.log('Started refreshing application (/) commands.');

    await rest.put
} catch (err) {
    console.log(err);
}
