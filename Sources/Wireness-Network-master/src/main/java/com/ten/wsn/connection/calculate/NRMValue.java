package com.ten.wsn.connection.calculate;

import com.ten.wsn.connection.WSNDispatcher;
import com.ten.wsn.connection.config.PositionInFrame;

import static com.ten.wsn.connection.config.FrameSize.*;

/**
 * 一条曲线上的点类型：（N,R,M）
 */
public class NRMValue implements PositionInFrame {

    private int n;
    private int r;
    private double mean;

    public void record(int n, int r, double mean) {
        this.n = n;
        this.r = r;
        this.mean = mean;
    }

    /**
     * FIXME Mapping NRM value to coordinate X
     */
    @Override
    public int getX() {
        return (int) ((double) this.getN() / WSNDispatcher.getVertexMaxRediu() * WIDTH * 5 + ORIGIN_X);
    }

    /**
     * FIXME Mapping NRM value to coordinate Y
     */
    @Override
    public int getY() {
        return (Y_AXIS_Y - (int) (this.getMean() * HEIGHT));
    }

    @Override
    public String toString() {
        return "NRMValue{" +
                "n=" + n +
                ", r=" + r +
                ", mean=" + mean +
                '}';
    }

    public int getN() {
        return n;
    }

    public int getR() {
        return r;
    }

    public void setN(int n) {
        this.n = n;
    }

    public void setR(int r) {
        this.r = r;
    }

    public double getMean() {
        return mean;
    }

}
