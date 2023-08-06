import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin,
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { showOnboarding } from './onboarding/showOnboarding';
import {
    drawSnippets,
    isLoading,
    PiecesView,
    setIsLoading,
} from './ui/piecesView';
import { loadPieces } from './connection/api_wrapper';
import '../style/icons.css';
import '../style/prism.css';
import '../style/images.css';
import { getStored, setStored } from './localStorageManager';
import { createCommands } from './actions/create_commands';
import { stopPolling } from './connection/poll_for_new_snippets';
import * as Sentry from '@sentry/browser';
import { SentryTracking } from './analytics/SentryTracking';
import {
    CapabilitiesEnum,
    ConfigurationParameters,
} from './PiecesSDK/connector';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import ConnectorSingleton from './connection/connector_singleton';
const config: ConnectorSingleton = ConnectorSingleton.getInstance();
import { SegmentAnalytics } from './analytics/SegmentAnalytics';
import { Heartbeat, pluginActivityCheck } from './analytics/Heartbeat';
import { IStateDB } from '@jupyterlab/statedb';
import { ReadonlyJSONObject } from '@lumino/coreutils';
import PiecesCacheSingleton from './cache/pieces_cache';
import { Asset } from './PiecesSDK/core';

/**
 * Initialization data for the jupyter-pieces extension.
 */
export const PLUGIN_ID = 'jupyter-pieces';
export let defaultApp: JupyterFrontEnd;
export let defaultView: PiecesView;
export let theme: string;

export const pluginHeartbeat = new Heartbeat(5); // 5 minutes

// Getting rid of stupid TS squiggles that aren't actually issues
// @ts-ignore
const plugin: JupyterFrontEndPlugin<void> = {
    id: PLUGIN_ID + ':plugin',
    description:
        'Pieces for Developers is a code snippet management tool powered by AI.',
    autoStart: true,
    //@ts-ignore
    requires: [ICommandPalette, IStateDB],
    optional: [],
    deactivate: async () => {
        stopPolling();

        await Sentry.close(2000);

        pluginHeartbeat.stop();
    },
    activate: async (
        app: JupyterFrontEnd,
        palette: ICommandPalette,
        state: IStateDB
    ) => {
        const cache = PiecesCacheSingleton.getInstance();
        app.restored.then(async () => {
            const assets = (await state.fetch(PLUGIN_ID)) as unknown as Asset[];
            if (!isLoading) {
                return;
            }
            assets.forEach(
                (val) => (val.created.value = new Date(val.created.value))
            );
            cache.store({ assets: assets as unknown as Asset[] });
            setIsLoading(false);
            drawSnippets({});
        });
        theme = '';
        defaultApp = app;
        const piecesView = new PiecesView();
        defaultView = piecesView;
        piecesView.build(app);
        createCommands({ palette });
        loadPieces()
            .catch((error) => {
                console.error('Pieces loading error!', error);
            })
            .finally(() => {
                if (!getStored('onBoardingShown')) {
                    showOnboarding();
                    setStored({ onBoardingShown: true });
                }
                setIsLoading(false);
                drawSnippets({});
                const assets = cache.assets;
                app.restored.then(() => {
                    state.save(
                        PLUGIN_ID,
                        assets as unknown as ReadonlyJSONObject
                    );
                });
            });

        SentryTracking.init();
        SegmentAnalytics.init();

        pluginHeartbeat.start(() => {
            pluginActivityCheck();
        });

        console.log('updated15');

        console.log(`Successfully loaded '${PLUGIN_ID}'`);

        document.body.addEventListener('click', () => {
            if (theme !== document.body.getAttribute('data-jp-theme-light')) {
                theme = document.body.getAttribute('data-jp-theme-light')!;
                drawSnippets({});
            }
        });
    },
};

// Getting rid of stupid TS squiggles that aren't actually issues
// @ts-ignore
const settings: JupyterFrontEndPlugin<void> = {
    id: PLUGIN_ID + ':pieces-settings',
    description:
        'Pieces for Developers is a code snippet management tool powered by AI.',
    autoStart: true,
    requires: [ISettingRegistry],
    optional: [],
    activate: async (app: JupyterFrontEnd, settings: ISettingRegistry) => {
        function loadSetting(settings: ISettingRegistry.ISettings): void {
            // Read the settings and convert to the correct type
            if (
                getStored('AutoOpen') !==
                (settings.get('AutoOpen').composite as boolean)
            ) {
                setStored({
                    AutoOpen: settings.get('AutoOpen').composite as boolean,
                });
            }

            if (
                getStored('Port') !== (settings.get('Port').composite as number)
            ) {
                setStored({
                    Port: settings.get('Port').composite as number,
                });
                const ConfigParams: ConfigurationParameters = {
                    basePath: `http://localhost:${
                        settings.get('Port').composite as number
                    }`,
                    fetchApi: fetch,
                };
                config.parameters = ConfigParams;
            }

            if (
                getStored('Capabilities') !==
                (settings.get('Capabilities').composite as string).toUpperCase()
            ) {
                switch (settings.get('Capabilities').composite as string) {
                    case 'Local':
                        setStored({
                            Capabilities: CapabilitiesEnum.Local,
                        });
                        break;
                    case 'Blended':
                        setStored({
                            Capabilities: CapabilitiesEnum.Blended,
                        });
                        break;
                    case 'Cloud':
                        setStored({
                            Capabilities: CapabilitiesEnum.Cloud,
                        });
                        break;
                    default:
                        setStored({
                            Capabilities: CapabilitiesEnum.Blended,
                        });
                        break;
                }
                config.application.capabilities = getStored('Capabilities');
            }
        }

        // Wait for the application to be restored and
        // for the settings for this plugin to be loaded
        Promise.all([
            app.restored,
            //@ts-ignore
            settings.load(PLUGIN_ID + ':pieces-settings'),
        ])
            .then(([, settings]) => {
                // Read the settings
                if (settings) {
                    loadSetting(settings);
                }

                // Listen for your plugin setting changes using Signal
                settings.changed.connect(loadSetting);
            })
            .catch((reason) => {
                console.error(
                    `Something went wrong when reading the settings.\n${reason}`
                );
            });
    },
};

export default [settings, plugin];
