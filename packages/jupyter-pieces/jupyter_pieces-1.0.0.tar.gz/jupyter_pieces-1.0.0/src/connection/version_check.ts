import Notifications from './notification_handler';
import ConnectorSingleton from './connector_singleton';
import Constants from '../const';
import { launchRuntime } from '../actions/launch_runtime';
import { gt, lt } from 'semver';

const notifications: Notifications = Notifications.getInstance();
const config: ConnectorSingleton = ConnectorSingleton.getInstance();

export default async function versionCheck({
    retry,
    minVersion,
}: {
    retry?: boolean;
    minVersion?: string;
}): Promise<boolean> {
    try {
        const osVersion: string =
            await config.wellKnownApi.getWellKnownVersion();
        if (osVersion.includes('staging')) return true;

        const osUpdated =
            gt(osVersion, minVersion ?? '4.9.9') && lt(osVersion, '6.0.0');

        if (!osUpdated) {
            notifications.error({ message: Constants.UPDATE_OS });
        }

        return osUpdated;
    } catch (error: any) {
        if (retry) {
            return false;
        }
        if (error.code === 'ECONNREFUSED') {
            await launchRuntime(true);
        }
        return await versionCheck({ retry: true });
    }
}
