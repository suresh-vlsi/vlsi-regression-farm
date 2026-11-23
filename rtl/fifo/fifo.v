// Synchronous FIFO
module fifo #(parameter WIDTH = 8, parameter DEPTH = 16) (
    input  wire             clk,
    input  wire             rst_n,
    input  wire             wr_en,
    input  wire [WIDTH-1:0] din,
    input  wire             rd_en,
    output reg  [WIDTH-1:0] dout,
    output wire             full,
    output wire             empty
);
    localparam AW = $clog2(DEPTH);
    reg [WIDTH-1:0] mem [0:DEPTH-1];
    reg [AW:0] wptr, rptr;

    assign empty = (wptr == rptr);
    assign full  = (wptr[AW] != rptr[AW]) && (wptr[AW-1:0] == rptr[AW-1:0]);

    always @(posedge clk) begin
        if (!rst_n) begin
            wptr <= 0; rptr <= 0; dout <= 0;
        end else begin
            if (wr_en && !full) begin
                mem[wptr[AW-1:0]] <= din;
                wptr <= wptr + 1'b1;
            end
            if (rd_en && !empty) begin
                dout <= mem[rptr[AW-1:0]];
                rptr <= rptr + 1'b1;
            end
        end
    end
endmodule
