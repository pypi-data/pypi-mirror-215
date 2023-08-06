import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { showDialog, Dialog, MainAreaWidget } from '@jupyterlab/apputils';
import { runIcon } from '@jupyterlab/ui-components';

import { requestAPI } from './handler';

import { RunsPanelWidget } from './widgets/RunsPanelWidget';
/**
 * Initialization data for the nbconvert_queue extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'nbconvert_queue:plugin',
  description: 'A JupyterLab extension for queuing notebooks executions.',
  autoStart: true,
  requires: [IFileBrowserFactory],
  activate: (app: JupyterFrontEnd, factory: IFileBrowserFactory) => {
    const runsContent = new RunsPanelWidget();
    runsContent.addClass('jp-PropertyInspector-placeholderContent');
    const runsWidget = new MainAreaWidget<RunsPanelWidget>({
      content: runsContent
    });
    runsWidget.toolbar.hide();
    runsWidget.title.icon = runIcon;
    runsWidget.title.caption = 'Nbconvert runs';
    app.shell.add(runsWidget, 'right', { rank: 501 });

    app.commands.addCommand('nbconvert_queue:open', {
      label: 'Run',
      caption: "Example context menu button for file browser's items.",
      icon: runIcon,
      execute: () => {
        console.log('nbconvert_queue:open');
        const file = factory.tracker.currentWidget?.selectedItems().next();

        console.log(JSON.parse(JSON.stringify(file)));
        const obj = JSON.parse(JSON.stringify(file));

        if (obj) {
          showDialog({
            title: obj.name,
            body: 'Path: ' + obj.path,
            buttons: [Dialog.okButton()]
          }).catch(e => console.log(e));
        }

        requestAPI<any>('run', {
          method: 'POST',
          body: JSON.stringify({ notebook: obj.path })
        })
          .then(data => {
            console.log(data);
          })
          .catch(reason => {
            console.error(
              `The nbconvert_queue server extension appears to be missing.\n${reason}`
            );
          });
      }
    });

    app.contextMenu.addItem({
      command: 'nbconvert_queue:open',
      selector: '.jp-DirListing-item[data-isdir="false"]',
      rank: 0
    });
  }
};
export default plugin;
