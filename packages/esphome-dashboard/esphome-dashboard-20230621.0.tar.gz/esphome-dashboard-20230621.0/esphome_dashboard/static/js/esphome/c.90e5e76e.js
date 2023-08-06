import{r as t,b as o,d as e,l as s,n as i,s as n,y as r,I as a}from"./index-bfcf9cd9.js";import"./c.22fb066b.js";import{o as l}from"./c.d861da54.js";import"./c.4971d925.js";let c=class extends n{render(){return r`
      <esphome-process-dialog
        .heading=${`Install ${this.configuration}`}
        .type=${"run"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${"OTA"===this.target?"":r`
              <a
                href="https://esphome.io/guides/faq.html#i-can-t-get-flashing-over-usb-to-work"
                slot="secondaryAction"
                target="_blank"
                >❓</a
              >
            `}
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":r`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){a(this.configuration)}_handleProcessDone(t){this._result=t.detail}_handleRetry(){l(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};c.styles=t`
    a[slot="secondaryAction"] {
      text-decoration: none;
      line-height: 32px;
    }
  `,o([e()],c.prototype,"configuration",void 0),o([e()],c.prototype,"target",void 0),o([s()],c.prototype,"_result",void 0),c=o([i("esphome-install-server-dialog")],c);
