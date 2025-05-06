import { join } from 'path';
import { format } from 'url';

import { BrowserWindow, app } from 'electron';
import isDev from 'electron-is-dev';
import prepareNext from 'electron-next';

app.on('ready', async () => {
    await prepareNext('./renderer');

    const mainWindow = new BrowserWindow({
        title: 'RaizouRaider Next',
        autoHideMenuBar: true,
        width: 816,
        height: 512,
        resizable: false,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: join(__dirname, 'preload.js'),
        },
    });

    const url = isDev
        ? 'http://localhost:8000/'
        : format({
              pathname: join(__dirname, '../renderer/out/index.html'),
              protocol: 'file:',
              slashes: true,
          });

    mainWindow.loadURL(url);
});

app.on('window-all-closed', app.quit);
