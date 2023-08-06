"use strict";
(self["webpackChunkjupyterlab_empinken_extension"] = self["webpackChunkjupyterlab_empinken_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
//import {CellList} from '@jupyterlab/notebook'; //gets list from ISharedNotebook
//import { Cell } from '@jupyterlab/cells';

// Remove items in first list from second list
function removeListMembers(list1, list2) {
    return list2.filter(item => !list1.includes(item));
}
/**
 * The plugin registration information.
 */
// https://jupyterlab.readthedocs.io/en/stable/api/index.html
// https://jupyterlab.readthedocs.io/en/3.3.x/api/interfaces/notebook.inotebooktracker.html
const empinken_tags = ["activity", "learner", "solution", "tutor"];
const plugin = {
    id: 'jupyterlab_empinken_extension:plugin',
    description: 'A JupyterLab extension adding a button to the Notebook toolbar.',
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    autoStart: true,
    activate: (app, notebookTracker) => {
        const { commands } = app;
        //labshell via https://discourse.jupyter.org/t/jupyterlab-4-iterating-over-all-cells-in-a-notebook/20033/2
        const labShell = app.shell;
        labShell.currentChanged.connect(() => {
            const notebook = app.shell.currentWidget;
            if (notebook) {
                notebook.revealed.then(() => {
                    var _a;
                    (_a = notebook.content.widgets) === null || _a === void 0 ? void 0 : _a.forEach(cell => {
                        var _a;
                        const tagList = (_a = cell.model.getMetadata('tags')) !== null && _a !== void 0 ? _a : [];
                        console.log("cell metadata", tagList);
                        tagList.forEach((tag) => {
                            var _a;
                            if (empinken_tags.includes(tag)) {
                                //console.log("hit",tag)
                                (_a = cell.node) === null || _a === void 0 ? void 0 : _a.classList.add('iou-' + tag + '-node');
                            }
                        });
                    });
                    //const cellList = notebook.content.model.cells;
                    //let i=1;
                    //for (const cell of cellList) {
                    //  console.log("a cell of type", cell.type, i)
                    //const tagList = convertToList(cell.metadata.tags);
                    //empinken_tags.forEach((tag) => {
                    //  if (tagList?.includes(tag)) {
                    //    console.log("hit",tag)
                    //    //cell.node.classList.add('iou-activity-node');
                    //  }
                    //})
                    //i=i+1;
                    //console.log('METADATA: ', cell.metadata)
                    //}
                });
            }
        });
        // if we can get a list of cells, then update on render?
        // https://jupyterlab.readthedocs.io/en/stable/api/classes/cells.Cell-1.html#ready
        // notebookTracker.currentChanged.connect((tracker, panel) => {
        //   //console.log(panel);
        //   if (!panel) {
        //     return;
        //   }
        //   console.log("fired on currentChanged")
        //   console.log("this is the panel", panel)
        //   const nb = notebookTracker.currentWidget.content
        //   nb.widgets.forEach((cell: Cell) => {
        //     console.log("try",cell.model.type)
        //   })
        //   console.log("panel widgets length",panel.content.widgets.length)
        //   // Iterate over all cells in the notebook and display metadata for each cell
        //   // NO - this is only length 1?
        //   console.log("tracker widgets length",tracker.currentWidget.content.widgets.length)
        //   panel.content.widgets.forEach(cell=>{
        //     console.log("panel cell is", cell)
        //     if ( cell !== null) {
        //       //this doesn't work wrt metadata
        //       console.log(cell.model.type)
        //       if (cell.model.type === 'code' || cell.model.type === 'markdown') {
        //         //console.log("tags",cell.model?.getMetadata('tags'))
        //         let tagList = cell.model.getMetadata("tags") as string[] ?? [];
        //         console.log("model here is", cell.model);
        //         console.log("metadata tags here is", tagList);
        //         if (tagList?.includes('activity')) {
        //           cell.node.classList.add('iou-activity-node');
        //         }
        //         //console.log(cell.model.type)
        //         //console.log(cell.model.metadata)
        //         //console.log(cell.model.metadata.get('tags'))
        //         //console.log(cell.model.metadata.get('tags').includes('activity'))
        //         //co
        //       }
        //     }
        //   })
        // });
        // TO DO  - if the notebook tracker points to current cell
        // then we should be able to get the current cell.
        const createEmpinkenCommand = (label, type) => {
            //this works wrt metadata
            const caption = `Execute empinken ${type} Command`;
            return {
                label,
                caption,
                execute: () => {
                    var _a;
                    let activeCell = notebookTracker.activeCell;
                    //console.log(label, type, caption)
                    //console.log(activeCell)
                    const nodeclass = 'iou-' + type + "-node";
                    if (activeCell !== null) {
                        let tagList = (_a = activeCell.model.getMetadata("tags")) !== null && _a !== void 0 ? _a : [];
                        //console.log("cell metadata was", tagList, "; checking for", type);
                        if (tagList.includes(type)) {
                            // ...then remove it
                            const index = tagList.indexOf(type, 0);
                            if (index > -1) {
                                tagList.splice(index, 1);
                            }
                            activeCell.model.setMetadata("tags", tagList);
                            // Remove class
                            activeCell.node.classList.remove(nodeclass);
                            // cell.node.classList exists
                        }
                        else {
                            // remove other tags
                            tagList = removeListMembers(empinken_tags, tagList);
                            empinken_tags.forEach((tag) => {
                                activeCell.node.classList.remove('iou-' + tag + "-node");
                            });
                            // add required tag
                            tagList.push(type);
                            activeCell.model.setMetadata("tags", tagList);
                            activeCell.node.classList.add(nodeclass);
                        }
                        //console.log("cell metadata now is", tagList);
                    }
                }
            };
        };
        // empinken_tags.forEach((tag:string) => {
        //   commands.addCommand('ouseful-empinken:'+tag,
        //     createEmpinkenCommand(tag.charAt(0).toUpperCase(),
        //     tag));
        // })
        const command_a = 'ouseful-empinken:activity';
        const command_l = 'ouseful-empinken:learner';
        const command_s = 'ouseful-empinken:solution';
        const command_t = 'ouseful-empinken:tutor';
        // Add commands
        commands.addCommand(command_a, createEmpinkenCommand('A', 'activity'));
        commands.addCommand(command_l, createEmpinkenCommand('L', 'learner'));
        commands.addCommand(command_s, createEmpinkenCommand('S', 'solution'));
        commands.addCommand(command_t, createEmpinkenCommand('T', 'tutor'));
        console.log("commands added");
        // Call the command execution
        //commands.execute(command_a, { origin: 'init' }).catch(reason => {
        //  console.error(
        //    `An error occurred during the execution of empinken-A.\n${reason}`
        //  );
        //});
    }
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.2f2d08c0aa32ccae54d5.js.map